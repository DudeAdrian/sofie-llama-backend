# S.O.F.I.E. Wellness Backend

**S**entient **O**rchestrator **F**or **I**ntegrated **E**vidence-based wellness

A modular, privacy-first backend for the S.O.F.I.E. Wellness Operating System. Built with Python, FastAPI, and LLaMA for context-aware, consent-based wellness guidance.

## 🌟 Core Principles

- **Regulation-before-reasoning**: Consent checks happen before any AI computation
- **Consent-before-computation**: Explicit user consent required for all operations
- **Privacy-first**: Local-first architecture with minimal data collection
- **Modular**: Clean separation of concerns for easy extension
- **Evidence-based**: Grounded in wellness research and best practices

## 🏗️ Architecture

```
sofie-llama-backend/
├── app/
│   ├── config/          # Configuration and settings
│   ├── middleware/      # Request processing and consent enforcement
│   ├── models/          # Pydantic schemas for validation
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic (consent, LLaMA)
│   └── main.py          # FastAPI application entry point
├── models/              # LLaMA model files (.gguf)
├── requirements.txt     # Python dependencies
└── .env.example        # Environment configuration template
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- 4GB+ RAM (for running LLaMA models)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DudeAdrian/sofie-llama-backend.git
   cd sofie-llama-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

5. **Download a LLaMA model** (optional but recommended)
   
   Download a LLaMA model in GGUF format (e.g., [llama-2-7b-chat.gguf](https://huggingface.co/TheBloke)) and place it in the `models/` directory:
   
   ```bash
   mkdir -p models
   # Place your .gguf model file in models/
   # Update LLAMA_MODEL_PATH in .env to point to your model
   ```
   
   **Note**: The backend works without a model (provides mock responses) for testing.

6. **Run the server**
   ```bash
   python -m app.main
   # Or use uvicorn directly:
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

7. **Access the API**
   - API docs (Swagger): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc
   - Health check: http://localhost:8000/api/v1/health

## 📖 Usage

### 1. Check Service Health

```bash
curl http://localhost:8000/api/v1/health
```

### 2. Grant Consent

Before requesting wellness guidance, users must grant consent:

```bash
curl -X POST http://localhost:8000/api/v1/consent/grant \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "consent_type": "wellness_guidance",
    "purpose": "Receive personalized wellness guidance"
  }'
```

### 3. Request Wellness Guidance

Once consent is granted, request guidance:

```bash
curl -X POST http://localhost:8000/api/v1/wellness/guidance \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "query": "What are some gentle exercises for stress reduction?",
    "context": {
      "mood": "anxious",
      "stress_level": 7,
      "energy_level": 5,
      "goals": ["reduce stress", "improve sleep"]
    }
  }'
```

### 4. Check Consent Status

```bash
curl http://localhost:8000/api/v1/consent/check/user_123/wellness_guidance
```

### 5. Revoke Consent

Users can revoke consent at any time:

```bash
curl -X DELETE http://localhost:8000/api/v1/consent/revoke/user_123/wellness_guidance
```

## 🔧 Configuration

Edit `.env` to customize the backend:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host address | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `ENVIRONMENT` | Environment (development/production) | `development` |
| `LLAMA_MODEL_PATH` | Path to LLaMA model file | `models/llama-2-7b-chat.gguf` |
| `LLAMA_N_CTX` | LLaMA context window size | `2048` |
| `LLAMA_TEMPERATURE` | LLaMA sampling temperature | `0.7` |
| `REQUIRE_CONSENT` | Enforce consent checks | `true` |
| `CONSENT_EXPIRY_HOURS` | Hours until consent expires | `24` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🔌 API Endpoints

### Health & Status
- `GET /api/v1/health` - Check service health and capabilities

### Consent Management
- `POST /api/v1/consent/grant` - Grant consent for an operation
- `GET /api/v1/consent/check/{user_id}/{consent_type}` - Check consent status
- `DELETE /api/v1/consent/revoke/{user_id}/{consent_type}` - Revoke consent

### Wellness Guidance
- `POST /api/v1/wellness/guidance` - Get AI-powered wellness guidance (requires consent)

## 🧩 Extending the Backend

### Adding New Endpoints

1. Create a new router in `app/routers/`:
   ```python
   from fastapi import APIRouter
   
   router = APIRouter(prefix="/api/v1/myfeature", tags=["myfeature"])
   
   @router.get("/")
   async def my_endpoint():
       return {"message": "Hello"}
   ```

2. Register the router in `app/main.py`:
   ```python
   from app.routers import myfeature
   app.include_router(myfeature.router)
   ```

### Adding New Consent Types

1. Update `ConsentType` enum in `app/models/schemas.py`:
   ```python
   class ConsentType(str, Enum):
       WELLNESS_GUIDANCE = "wellness_guidance"
       MY_NEW_TYPE = "my_new_type"
   ```

2. Enforce consent in your endpoint:
   ```python
   from app.services import consent_manager
   from app.models.schemas import ConsentType
   
   if not consent_manager.verify_or_deny(user_id, ConsentType.MY_NEW_TYPE):
       raise HTTPException(403, "Consent required")
   ```

### Adding New Services

1. Create service in `app/services/`:
   ```python
   class MyService:
       def do_something(self):
           pass
   
   my_service = MyService()
   ```

2. Export from `app/services/__init__.py`:
   ```python
   from app.services.my_service import my_service
   __all__ = [..., "my_service"]
   ```

## 🔒 Privacy & Security

- **No persistent storage by default**: Consent data is stored in-memory (use a database in production)
- **Consent expiration**: Consent automatically expires after configured hours
- **Local-first**: LLaMA runs locally, no data sent to external APIs
- **CORS protection**: Configurable allowed origins
- **Logging**: All consent decisions are logged for audit

## 🧪 Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn app.main:app --reload

# Or
python -m app.main
```

### Project Structure Principles

- **Modular**: Each component has a single responsibility
- **Testable**: Services and routers are decoupled
- **Extensible**: Easy to add new features without modifying core code
- **Type-safe**: Pydantic models for request/response validation

## 📝 License

This project is open source. See LICENSE for details.

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Consent enforcement is maintained
- Privacy principles are respected
- Code follows the modular architecture
- Documentation is updated

## 📧 Contact

For questions or support, please open an issue on GitHub.
