import os
import joblib
import numpy as np
from config import Config

_models = {}
_scalers = {}
_encoders = {}

def _get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def _get_parent_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_models():
    global _models, _scalers, _encoders

    models_dir = os.path.join(_get_parent_dir(), 'models')

    _models['career'] = joblib.load(os.path.join(models_dir, 'career_model.pkl'))
    _scalers['career'] = joblib.load(os.path.join(models_dir, 'career_scaler.pkl'))
    _encoders['career'] = joblib.load(os.path.join(models_dir, 'career_label_encoder.pkl'))

    _models['performance'] = joblib.load(os.path.join(models_dir, 'performance_model.pkl'))
    _scalers['performance'] = joblib.load(os.path.join(models_dir, 'performance_scaler.pkl'))

    _models['stress'] = joblib.load(os.path.join(models_dir, 'stress_model.pkl'))
    _encoders['stress'] = joblib.load(os.path.join(models_dir, 'stress_features.pkl'))

def predict_career(data):
    """Predict career based on academic scores, skills, and RIASEC scores."""
    if 'career' not in _models:
        load_models()

    feature_names = [
        'Math_Score', 'Science_Score', 'Programming_Skill', 'Communication_Skill',
        'Logical_Ability', 'R_score', 'I_score', 'A_score', 'S_score', 'E_score', 'C_score'
    ]

    features = np.array([[data.get(f, 0) for f in feature_names]])

    scaled = _scalers['career'].transform(features)
    prediction = _models['career'].predict(scaled)
    probabilities = _models['career'].predict_proba(scaled)[0]

    predicted_class = prediction[0]
    predicted_career = _encoders['career'].inverse_transform([predicted_class])[0]
    confidence = probabilities[predicted_class] * 100

    return {
        'prediction': predicted_career,
        'confidence': round(confidence, 1),
        'all_probabilities': {
            _encoders['career'].inverse_transform([i])[0]: round(p * 100, 1)
            for i, p in enumerate(probabilities)
        }
    }

def predict_performance(data):
    """Predict final grade (G3) based on student features."""
    if 'performance' not in _models:
        load_models()

    feature_names = [
        'Unnamed: 0', 'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
        'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid',
        'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel',
        'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2',
        'Mjob_health', 'Mjob_other', 'Mjob_services', 'Mjob_teacher',
        'Fjob_health', 'Fjob_other', 'Fjob_services', 'Fjob_teacher',
        'reason_home', 'reason_other', 'reason_reputation',
        'guardian_mother', 'guardian_other', 'high_absences'
    ]

    features = np.array([[data.get(f, 0) for f in feature_names]])

    prediction = _models['performance'].predict(features)[0]

    grade = max(0, min(20, round(prediction, 0)))

    if grade >= 16:
        status = "Excellent"
    elif grade >= 14:
        status = "Good"
    elif grade >= 10:
        status = "Average"
    else:
        status = "Needs Improvement"

    return {
        'prediction': int(grade),
        'status': status,
        'scale_note': 'Grade is on a 0-20 scale (typical in Portuguese grading system)'
    }

def predict_stress(data):
    """Predict stress level based on various factors."""
    if 'stress' not in _models:
        load_models()

    feature_names = [
        'anxiety_level', 'self_esteem', 'mental_health_history', 'depression',
        'headache', 'blood_pressure', 'sleep_quality', 'breathing_problem',
        'noise_level', 'living_conditions', 'safety', 'basic_needs',
        'academic_performance', 'study_load', 'teacher_student_relationship',
        'future_career_concerns', 'social_support', 'peer_pressure',
        'extracurricular_activities', 'bullying'
    ]

    features = np.array([[data.get(f, 0) for f in feature_names]])

    raw_pred = _models['stress'].predict(features)
    prediction = int(raw_pred[0][0] if raw_pred.ndim > 1 else raw_pred[0])
    probabilities = _models['stress'].predict_proba(features)[0]

    levels = {0: 'Low', 1: 'Medium', 2: 'High'}
    predicted_level = levels.get(prediction, 'Unknown')
    confidence = probabilities[prediction] * 100

    return {
        'prediction': predicted_level,
        'confidence': round(confidence, 1),
        'all_probabilities': {
            levels[i]: round(p * 100, 1) for i, p in enumerate(probabilities)
        }
    }