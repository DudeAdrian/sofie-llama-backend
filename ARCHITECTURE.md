# S.O.F.I.E. Backend Architecture

## Overview

S.O.F.I.E. (Sentient Orchestrator for Integrated Evidence-based wellness) is a modular, privacy-first backend for wellness guidance, built with FastAPI and LLaMA.

## Core Architectural Principles

### 1. Regulation-before-Reasoning
Every AI computation is preceded by consent verification. The system enforces:
- Consent checks happen **before** any LLaMA inference
- No exceptions to the consent requirement
- All consent decisions are logged and auditable

### 2. Consent-before-Computation
Users must explicitly grant consent for operations:
- Consent is time-limited (configurable expiry)
- Users can revoke consent at any time
- Revocation immediately blocks further processing

### 3. Modular Architecture
Clean separation of concerns for maintainability and extensibility:
```
app/
├── config/           # Configuration management
├── middleware/       # Request/response processing
├── models/           # Data validation schemas
├── routers/          # API endpoints
└── services/         # Business logic
```

## Component Details

### Configuration Layer (`app/config/`)
- **Purpose**: Centralized configuration management
- **Key Features**:
  - Environment-based configuration via `.env`
  - Type-safe settings using Pydantic
  - Sensible defaults for all parameters
  
### Middleware Layer (`app/middleware/`)
- **Purpose**: Request/response processing and enforcement
- **Components**:
  - `ConsentEnforcementMiddleware`: Monitors protected endpoints
  - `LoggingMiddleware`: Logs all requests/responses
- **Key Features**:
  - CORS configuration for web clients
  - Request/response logging
  - Protected endpoint monitoring

### Models Layer (`app/models/`)
- **Purpose**: Data validation and serialization
- **Key Schemas**:
  - `ConsentRequest`/`ConsentResponse`: Consent management
  - `WellnessRequest`/`WellnessResponse`: Guidance requests
  - `WellnessContext`: User context information
- **Key Features**:
  - Type-safe validation using Pydantic
  - JSON schema generation for API docs
  - Example data for documentation

### Services Layer (`app/services/`)
The heart of the business logic:

#### Consent Service (`consent_service.py`)
- **Purpose**: Enforce consent-before-computation
- **Key Methods**:
  - `grant_consent()`: Grant user consent with expiry
  - `check_consent()`: Verify consent status
  - `revoke_consent()`: Immediately revoke consent
  - `verify_or_deny()`: Strict boolean check (used before computation)
- **Storage**: In-memory (replace with database in production)

#### LLaMA Service (`llama_service.py`)
- **Purpose**: AI-powered wellness guidance
- **Key Methods**:
  - `generate_wellness_guidance()`: Main inference method
  - `is_available()`: Check if model is loaded
  - `_build_wellness_prompt()`: Prompt engineering
  - `_generate_mock_guidance()`: Fallback when model unavailable
- **Key Features**:
  - Lazy model loading (only loads when needed)
  - Graceful degradation (mock responses if model missing)
  - Context-aware prompts
  - Evidence-based guidance focus

### Routers Layer (`app/routers/`)
REST API endpoints organized by domain:

#### Health Router (`health.py`)
- `GET /api/v1/health`: Service health check
- Returns: Service status, version, LLaMA availability, consent enforcement status

#### Consent Router (`consent.py`)
- `POST /api/v1/consent/grant`: Grant consent
- `GET /api/v1/consent/check/{user_id}/{consent_type}`: Check status
- `DELETE /api/v1/consent/revoke/{user_id}/{consent_type}`: Revoke consent

#### Wellness Router (`wellness.py`)
- `POST /api/v1/wellness/guidance`: Get AI guidance (requires consent)
- **Critical**: Enforces consent-before-computation at endpoint level

## Data Flow

### Wellness Guidance Request Flow

```
1. Client → POST /api/v1/wellness/guidance
   ↓
2. Middleware → Log request
   ↓
3. Router → Validate request schema (Pydantic)
   ↓
4. Router → verify_or_deny(user_id, WELLNESS_GUIDANCE)
   ↓
5a. Consent DENIED → Return 403 Forbidden
5b. Consent GRANTED → Continue
   ↓
6. LLaMA Service → Build context-aware prompt
   ↓
7. LLaMA Service → Generate guidance (or mock)
   ↓
8. Router → Format response with metadata
   ↓
9. Client ← Return wellness guidance
```

### Consent Enforcement Checkpoints

1. **Middleware**: Monitors protected endpoints
2. **Router**: Calls `verify_or_deny()` before computation
3. **Service**: Logs all consent decisions
4. **Response**: Includes `consent_verified: true` in response

## Extension Points

### Adding New Endpoints

1. Create router file: `app/routers/my_feature.py`
2. Define routes with FastAPI decorators
3. Register router in `app/main.py`
4. Add appropriate consent checks if needed

### Adding New Consent Types

1. Update `ConsentType` enum in `app/models/schemas.py`
2. Use `consent_manager.verify_or_deny()` in protected endpoints
3. Document consent purpose for transparency

### Adding New Services

1. Create service file: `app/services/my_service.py`
2. Implement service class with business logic
3. Export from `app/services/__init__.py`
4. Import and use in routers

### Replacing In-Memory Storage

The consent manager uses in-memory storage by default. For production:

1. Create database models (SQLAlchemy/SQLModel)
2. Update `ConsentManager` methods to use DB
3. Add database connection to `app/main.py`
4. Implement data migration scripts

## Security Considerations

### Current Security Features
- ✅ Consent enforcement before computation
- ✅ CORS protection with configurable origins
- ✅ Request/response logging for audit trails
- ✅ Input validation via Pydantic schemas
- ✅ No external API calls (local LLaMA)

### Production Recommendations
- [ ] Add authentication (OAuth2, JWT)
- [ ] Implement rate limiting
- [ ] Add HTTPS/TLS
- [ ] Use persistent database with encryption
- [ ] Add request ID tracking
- [ ] Implement user session management
- [ ] Add API key authentication
- [ ] Set up monitoring and alerting

## Performance Considerations

### Current Implementation
- In-memory consent storage (fast, not persistent)
- Lazy LLaMA model loading
- Single-threaded inference

### Scaling Recommendations
- Use Redis for consent storage (fast + persistent)
- Implement request queuing for LLaMA
- Add multiple LLaMA worker processes
- Use async/await throughout
- Add caching for common queries
- Implement connection pooling

## Privacy Features

1. **Local-first**: LLaMA runs locally, no data sent to external APIs
2. **Minimal Data**: Only essential data is processed
3. **Consent Transparency**: Clear purpose for each consent request
4. **Time-limited Consent**: Automatic expiry after configured hours
5. **Immediate Revocation**: Users can revoke consent instantly
6. **Audit Logs**: All consent decisions are logged

## Testing Strategy

### Current Tests
- ✅ Manual API testing via `test_api.py`
- ✅ Full consent workflow validation
- ✅ Health check endpoint

### Recommended Tests
- Unit tests for each service
- Integration tests for API endpoints
- Consent enforcement edge cases
- LLaMA service with/without model
- Invalid input handling
- Performance/load testing

## Deployment

### Development
```bash
python -m app.main
# or
uvicorn app.main:app --reload
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
# or use gunicorn with uvicorn workers:
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000
```

### Docker (Recommended)
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring

### Key Metrics to Track
- Request latency
- Consent grant/deny rates
- LLaMA inference time
- Error rates by endpoint
- Active user sessions
- Model availability

### Logging
All logs include:
- Timestamp
- Log level
- Component name
- User ID (when applicable)
- Action performed
- Outcome

## Future Enhancements

1. **Database Integration**: Replace in-memory storage
2. **Authentication**: Add user authentication
3. **Multiple Models**: Support different LLaMA variants
4. **Websockets**: Real-time streaming responses
5. **Background Jobs**: Async processing queue
6. **Analytics**: Aggregate (anonymous) usage statistics
7. **Multi-language**: I18n support
8. **Model Fine-tuning**: Custom wellness model training
