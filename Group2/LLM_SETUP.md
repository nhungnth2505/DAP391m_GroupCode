# LLM Configuration Guide

## Quick Setup (Windows)

1. Edit the `.env` file in the `Web` folder
2. Get a free API key from **https://console.groq.com/keys** (fastest, free tier)
3. Set `LLM_API_KEY` with your API key
4. Run the app:
```bash
python app.py
```

## Quick Setup (Linux/Mac)

```bash
export LLM_PROVIDER=groq
export LLM_API_KEY="your-groq-api-key"
export LLM_MODEL="llama-3.1-8b-instant"
python app.py
```

## Provider Details

| Provider | Endpoint | Fast Model | Notes |
|----------|----------|------------|-------|
| **Groq** (recommended) | `https://api.groq.com/openai/v1/chat/completions` | `llama-3.1-8b-instant` | Fast, free tier available |
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-3.5-turbo` | Standard OpenAI API |
| **NVIDIA NIM** | `https://integrate.api.nvidia.com/v1/chat/completions` | `nvidia/mistral-nemo-mini-instruct` | Requires NIM-enabled account |
| **Azure** | Set manually | - | Requires full Azure endpoint URL |
| **Ollama** | `http://localhost:11434/v1/chat/completions` | `llama3.2` | Local models, no API key needed |

## Groq Models (Recommended)

For student chat, Groq's free tier offers fast responses:

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `llama-3.1-8b-instant` | ⚡⚡⚡⚡⚡ | ★★★☆☆ | Fast responses, simple queries |
| `mixtral-8x7b-32768` | ⚡⚡⚡⚡ | ★★★★☆ | Longer context, better reasoning |
| `llama-3.1-70b-versatile` | ⚡⚡⚡ | ★★★★★ | Complex reasoning, detailed answers |

## NVIDIA NIM Note

NVIDIA NIM requires a specific NIM-enabled API key. If you get "Function not found" errors, your key may not have NIM access. Use Groq instead for easier setup.