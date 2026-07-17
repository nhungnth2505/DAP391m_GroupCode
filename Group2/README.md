# DAP391m_GroupCode — StudentPath

AI-powered student guidance dashboard combining multi-model ML predictions with an intelligent chatbot advisor.

## Overview

StudentPath helps university students understand their academic journey through four modules:

| Module | Description | Model |
|--------|-------------|-------|
| **Career Prediction** | Discover ideal career path using RIASEC personality profiling + academic scores | CatBoost / Gradient Boosting |
| **Performance Prediction** | Forecast final grade (G3) from 30+ demographic, family, lifestyle & academic factors | Ensemble |
| **Stress Level** | Assess stress across psychological, physical, environmental, academic & social dimensions | CatBoost |
| **AI Advisor** | Context-aware chatbot that knows your prediction history — psychology counselor style | LLM (OpenAI-compatible) |

## Architecture

```
Survey Input → Preprocessing → ML Models → Prediction → Context Builder → LLM Advisor
```

- **9 classifiers** evaluated per task: SVM, CatBoost, LightGBM, XGBoost, Random Forest, Gradient Boosting, AdaBoost, Bagging, Decision Tree
- **Feature engineering**: SelectKBest, RFECV, PCA dimensionality reduction
- **LLM**: Answers only career, academic & stress questions — short, empathetic, psychology-counselor style

## Tech Stack

- **Backend**: Flask (Python)
- **ML**: scikit-learn, CatBoost, joblib
- **Frontend**: Vanilla HTML/CSS/JS, Fraunces + Plus Jakarta Sans fonts
- **LLM**: OpenAI-compatible API (Groq, NVIDIA, OpenAI, Azure, Ollama)

## Quick Start

```bash
# Clone
git clone https://github.com/nhungnth2505/DAP391m_GroupCode.git
cd DAP391m_GroupCode
git checkout Group2

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure LLM
cp .env.example .env
# Edit .env with your API key

# Run
python app.py
# Open http://localhost:5000
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (`groq`, `openai`, `nvidia`, `azure`, `ollama`) | `groq` |
| `LLM_API_KEY` | API key for the provider | — |
| `LLM_MODEL` | Model name | `llama-3.1-8b-instant` |
| `LLM_API_ENDPOINT` | Custom API endpoint | Provider default |
| `SECRET_KEY` | Flask secret key | Auto-generated |

## Project Structure

```
Web/
├── app.py                  # Flask application
├── config.py               # Configuration & LLM system prompt
├── models/                  # Trained ML models
├── static/
│   ├── css/style.css       # Stylesheet
│   └── js/app.js           # Client-side JS (charts, sliders, sample data)
├── templates/
│   ├── landing.html        # Home page with architecture diagram
│   ├── base.html           # Sidebar layout for module pages
│   ├── career.html         # Career prediction
│   ├── performance.html    # Performance prediction
│   ├── stress.html         # Stress prediction
│   └── chat.html           # AI advisor chat
├── utils/
│   ├── models.py           # Model loading & prediction
│   ├── history.py          # Session history management
│   └── llm.py              # LLM API interaction
└── requirements.txt
```

## License

This project is part of the DAP391m course at FPT University. All rights reserved.
