import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-student-dashboard-2024'

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    CAREER_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'career_model.pkl')
    CAREER_SCALER_PATH = os.path.join(BASE_DIR, 'models', 'career_scaler.pkl')
    CAREER_ENCODER_PATH = os.path.join(BASE_DIR, 'models', 'career_label_encoder.pkl')

    PERFORMANCE_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'performance_model.pkl')
    PERFORMANCE_SCALER_PATH = os.path.join(BASE_DIR, 'models', 'performance_scaler.pkl')

    STRESS_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'stress_model.pkl')
    STRESS_FEATURES_PATH = os.path.join(BASE_DIR, 'models', 'stress_features.pkl')

    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'groq')
    LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
    LLM_API_ENDPOINT = os.environ.get('LLM_API_ENDPOINT', 'https://api.groq.com/openai/v1/chat/completions')
    LLM_MODEL = os.environ.get('LLM_MODEL', 'llama-3.1-8b-instant')

    LLM_SYSTEM_PROMPT = os.environ.get('LLM_SYSTEM_PROMPT', '''You are a compassionate psychology counselor at a university student support center. Your role is to help university students with:

1. CAREER GUIDANCE — Career path recommendations, job roles (Software Engineer, Data Scientist, Doctor, Teacher, Accountant, Entrepreneur), RIASEC personality types, skill development.

2. ACADEMIC PERFORMANCE — Study strategies, grade improvement, time management, learning techniques, exam preparation.

3. STRESS MANAGEMENT — Stress levels (Low/Medium/High), anxiety, depression, sleep quality, work-life balance, mental well-being, coping strategies.

YOUR STYLE:
- You are a warm, empathetic psychology teacher — not a robot. Use simple, caring language.
- Keep every response SHORT: 2-4 sentences maximum. Be direct and actionable.
- Ask follow-up questions when appropriate to understand the student better.
- Use the student's prediction history (provided in context) to personalize advice.
- If a student shows signs of crisis, gently encourage professional help in one sentence.

STRICT RULES:
- ONLY answer about career, academic performance, and stress management.
- If asked ANYTHING else, respond EXACTLY: "Xin lỗi, mình chỉ có thể tư vấn về nghề nghiệp, học tập và quản lý căng thẳng thôi. Bạn cần mình giúp gì về những chủ đề này không?"
- Never make up information — only use what is provided in the context.''')


LLM_PROVIDER_CONFIGS = {
    'openai': {
        'api_key_env': 'OPENAI_API_KEY',
        'endpoint': 'https://api.openai.com/v1/chat/completions',
        'default_model': 'gpt-3.5-turbo',
        'models': ['gpt-3.5-turbo', 'gpt-4o-mini', 'gpt-4o']
    },
    'nvidia': {
        'api_key_env': 'NVIDIA_API_KEY',
        'endpoint': 'https://integrate.api.nvidia.com/v1/chat/completions',
        'default_model': 'nvidia/llama-3.1-nemotron-70b-instruct',
        'fast_model': 'nvidia/mistral-nemo-mini-instruct',
        'models': [
            'nvidia/llama-3.1-nemotron-70b-instruct',
            'nvidia/mistral-nemo-mini-instruct',
            'nvidia/aya-101',
            'nvidia/mixtral-8x7b-instruct-v0.1'
        ]
    },
    'azure': {
        'api_key_env': 'AZURE_OPENAI_KEY',
        'endpoint': '',  # Must be set manually: https://YOUR_RESOURCE.openai.azure.com/openai/deployments/YOUR_MODEL/chat/completions
        'default_model': '',
        'models': []
    },
    'ollama': {
        'api_key_env': None,
        'endpoint': 'http://localhost:11434/v1/chat/completions',
        'default_model': 'llama3.2',
        'models': []  # Depends on local installation
    },
    'groq': {
        'api_key_env': 'GROQ_API_KEY',
        'endpoint': 'https://api.groq.com/openai/v1/chat/completions',
        'default_model': 'llama-3.1-70b-versatile',
        'fast_model': 'llama-3.1-8b-instant',
        'models': ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']
    }
}


def get_llm_provider_config(provider=None):
    provider = provider or LLM_PROVIDER
    return LLM_PROVIDER_CONFIGS.get(provider, LLM_PROVIDER_CONFIGS['openai'])