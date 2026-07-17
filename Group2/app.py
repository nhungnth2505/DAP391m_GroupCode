from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import os

from config import Config
from utils.models import predict_career, predict_performance, predict_stress
from utils.history import (
    init_history, add_career_prediction, add_performance_prediction,
    add_stress_prediction, get_latest_predictions, build_llm_context
)
from utils.llm import get_llm_response

app = Flask(__name__)
app.config.from_object(Config)

@app.before_request
def ensure_history():
    if 'history' not in session:
        session['history'] = init_history()
    if 'chat_messages' not in session:
        session['chat_messages'] = []

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/demo')
def index():
    return redirect(url_for('career'))

@app.route('/career')
def career():
    return render_template('career.html', module='career')

@app.route('/performance')
def performance():
    return render_template('performance.html', module='performance')

@app.route('/stress')
def stress():
    return render_template('stress.html', module='stress')

@app.route('/chat')
def chat():
    history = session.get('history', {})
    context = build_llm_context(history)
    messages = session.get('chat_messages', [])
    return render_template('chat.html', module='chat', context=context, messages=messages)

@app.route('/api/career/predict', methods=['POST'])
def api_career_predict():
    data = request.get_json()

    required = ['Math_Score', 'Science_Score', 'Programming_Skill',
                'Communication_Skill', 'Logical_Ability',
                'R_score', 'I_score', 'A_score', 'S_score', 'E_score', 'C_score']

    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        result = predict_career(data)

        history = session.get('history', {})
        history = add_career_prediction(
            history,
            {k: data[k] for k in required},
            result['prediction'],
            result['confidence']
        )
        session['history'] = history

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance/predict', methods=['POST'])
def api_performance_predict():
    data = request.get_json()

    required = [
        'Unnamed: 0',
        'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
        'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid',
        'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel',
        'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences',
        'G1', 'G2',
        'Mjob_health', 'Mjob_other', 'Mjob_services', 'Mjob_teacher',
        'Fjob_health', 'Fjob_other', 'Fjob_services', 'Fjob_teacher',
        'reason_home', 'reason_other', 'reason_reputation',
        'guardian_mother', 'guardian_other', 'high_absences'
    ]

    input_data = {}
    for field in required:
        if field in data:
            input_data[field] = data[field]
        else:
            input_data[field] = 0

    try:
        result = predict_performance(input_data)

        history = session.get('history', {})
        history = add_performance_prediction(
            history,
            input_data,
            result['prediction'],
            result['status']
        )
        session['history'] = history

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stress/predict', methods=['POST'])
def api_stress_predict():
    data = request.get_json()

    required = [
        'anxiety_level', 'self_esteem', 'mental_health_history', 'depression',
        'headache', 'blood_pressure', 'sleep_quality', 'breathing_problem',
        'noise_level', 'living_conditions', 'safety', 'basic_needs',
        'academic_performance', 'study_load', 'teacher_student_relationship',
        'future_career_concerns', 'social_support', 'peer_pressure',
        'extracurricular_activities', 'bullying'
    ]

    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        result = predict_stress(data)

        history = session.get('history', {})
        history = add_stress_prediction(
            history,
            {k: data[k] for k in required},
            result['prediction'],
            result['confidence']
        )
        session['history'] = history

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/message', methods=['POST'])
def api_chat_message():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    messages = session.get('chat_messages', [])
    messages.append({'role': 'user', 'content': user_message})

    history = session.get('history', {})
    context = build_llm_context(history)

    system_prompt = Config.LLM_SYSTEM_PROMPT + f"\n\nUser Context:\n{context}"

    result = get_llm_response(messages, system_prompt)

    if 'error' in result:
        messages.append({'role': 'assistant', 'content': f"Sorry, I encountered an error: {result['error']}"})
    else:
        messages.append({'role': 'assistant', 'content': result['response']})

    session['chat_messages'] = messages

    return jsonify({
        'response': messages[-1]['content'],
        'messages': messages
    })

@app.route('/api/history', methods=['GET'])
def api_history():
    history = session.get('history', {})
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)