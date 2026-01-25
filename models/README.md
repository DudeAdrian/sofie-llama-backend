# LLaMA Models Directory

This directory is for storing LLaMA model files in GGUF format.

## Getting Started

1. **Download a LLaMA model** in GGUF format from HuggingFace:
   - [Llama-2-7B-Chat GGUF](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
   - Or other compatible models

2. **Place the model file here**:
   ```
   models/llama-2-7b-chat.gguf
   ```

3. **Update your .env file** to point to the model:
   ```
   LLAMA_MODEL_PATH=models/llama-2-7b-chat.gguf
   ```

## Model Requirements

- Format: GGUF (GGML Unified Format)
- Recommended: 7B parameter model for balance of quality and performance
- Minimum RAM: 4GB for 7B models, 8GB+ recommended

## Note

The backend will work without a model (providing mock responses) for testing purposes. However, for real wellness guidance, a LLaMA model is required.

## Example Models

- **llama-2-7b-chat.Q4_K_M.gguf** (~4GB) - Good balance
- **llama-2-13b-chat.Q4_K_M.gguf** (~7GB) - Better quality, needs more RAM
- **mistral-7b-instruct-v0.2.Q4_K_M.gguf** (~4GB) - Alternative model

Download from: https://huggingface.co/TheBloke
