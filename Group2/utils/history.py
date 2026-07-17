from datetime import datetime
import json

def init_history():
    return {
        'career': [],
        'performance': [],
        'stress': []
    }

def add_career_prediction(history, inputs, prediction, confidence):
    entry = {
        'timestamp': datetime.now().isoformat(),
        'inputs': inputs,
        'prediction': prediction,
        'confidence': confidence
    }
    history['career'].append(entry)
    return history

def add_performance_prediction(history, inputs, prediction, status):
    entry = {
        'timestamp': datetime.now().isoformat(),
        'inputs': inputs,
        'prediction': prediction,
        'status': status
    }
    history['performance'].append(entry)
    return history

def add_stress_prediction(history, inputs, prediction, confidence):
    entry = {
        'timestamp': datetime.now().isoformat(),
        'inputs': inputs,
        'prediction': prediction,
        'confidence': confidence
    }
    history['stress'].append(entry)
    return history

def get_latest_predictions(history):
    latest = {}
    if history['career']:
        latest['career'] = history['career'][-1]
    if history['performance']:
        latest['performance'] = history['performance'][-1]
    if history['stress']:
        latest['stress'] = history['stress'][-1]
    return latest

def build_llm_context(history):
    """Build a context string from user's prediction history for the LLM."""
    latest = get_latest_predictions(history)

    if not latest:
        return "The user hasn't used any prediction features yet."

    context_lines = ["Here is what I know about the user from their recent predictions:"]

    if 'career' in latest:
        c = latest['career']
        context_lines.append(
            f"- Career Prediction: {c['prediction']} (confidence: {c['confidence']}%)"
        )

    if 'performance' in latest:
        p = latest['performance']
        context_lines.append(
            f"- Performance Prediction: Grade {p['prediction']} ({p['status']})"
        )

    if 'stress' in latest:
        s = latest['stress']
        context_lines.append(
            f"- Stress Level Prediction: {s['prediction']} (confidence: {s['confidence']}%)"
        )

    context_lines.append(
        "\nUse this information to provide personalized advice to the student."
    )

    return "\n".join(context_lines)