# Ollama Local LLM Setup

Bypass HuggingFace authentication by using local Ollama.

## Quick Start

```bash
# 1. Install Ollama
# macOS/Linux:
curl -fsSL https://ollama.com/install.sh | sh

# Windows:
# Download from https://ollama.com/download/windows

# 2. Start Ollama
ollama serve

# 3. Pull model
ollama pull llama3.1:8b

# 4. Start Sofie-LLaMA with Ollama
export USE_OLLAMA=true
export OLLAMA_MODEL=llama3.1:8b
export OLLAMA_HOST=http://localhost:11434
python src/main.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_OLLAMA` | `false` | Enable Ollama mode |
| `OLLAMA_MODEL` | `llama3.1:8b` | Model name in Ollama |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint |

## Testing

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start with Ollama
USE_OLLAMA=true python src/main.py

# Should see:
# 🔧 Ollama mode detected - using local LLM
#    Ollama URL: http://localhost:11434
#    Model: llama3.1:8b
```

## Fallback Behavior

If HuggingFace fails with 401 auth error, the system automatically falls back to Ollama mode.

## Available Models

```bash
# List available models
ollama list

# Pull additional models
ollama pull llama3.1:70b    # Larger model
ollama pull mistral:latest   # Alternative model
ollama pull codellama:7b     # Code-focused
```

## Docker Compose

```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama
    
  sofie:
    build: .
    environment:
      - USE_OLLAMA=true
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - ollama
    ports:
      - "8000:8000"

volumes:
  ollama:
```

## Troubleshooting

### "Could not connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check port 11434 is not blocked
- Verify firewall settings

### "Model not found"
- Pull the model: `ollama pull llama3.1:8b`
- Check available models: `ollama list`

### Slow responses
- Use smaller model: `llama3.1:8b` instead of `70b`
- Check GPU availability
- Adjust Ollama GPU settings
