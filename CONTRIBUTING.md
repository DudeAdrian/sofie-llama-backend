# Contributing to S.O.F.I.E. Backend

Thank you for your interest in contributing to the S.O.F.I.E. Wellness Backend! This document provides guidelines for extending and improving the system.

## Core Principles

When contributing, please ensure your changes align with our core principles:

1. **Privacy First**: Always prioritize user privacy and data protection
2. **Consent Required**: Enforce consent-before-computation for all AI operations
3. **Modular Design**: Keep components loosely coupled and well-organized
4. **Evidence-based**: Ground wellness guidance in research and best practices
5. **Transparency**: Be clear about what the system does with user data

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy environment template:
   ```bash
   cp .env.example .env
   ```
5. Run the server:
   ```bash
   python -m app.main
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for function parameters and return values
- Add docstrings to classes and public methods
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Example

```python
from typing import Optional

def process_wellness_query(
    query: str, 
    user_id: str,
    context: Optional[WellnessContext] = None
) -> WellnessResponse:
    """
    Process a wellness query with consent verification.
    
    Args:
        query: User's wellness question
        user_id: Unique user identifier
        context: Optional user context for personalization
        
    Returns:
        WellnessResponse with AI-generated guidance
        
    Raises:
        HTTPException: If consent is not granted
    """
    # Implementation
```

## Project Structure

```
app/
├── config/          # Configuration management
├── middleware/      # Request/response processing
├── models/          # Pydantic schemas
├── routers/         # API endpoints
├── services/        # Business logic
└── main.py          # Application entry point
```

## Adding Features

### Adding a New Endpoint

1. **Create router file** (e.g., `app/routers/my_feature.py`):

```python
from fastapi import APIRouter
from app.models.schemas import MyRequest, MyResponse

router = APIRouter(prefix="/api/v1/myfeature", tags=["myfeature"])

@router.post("/", response_model=MyResponse)
async def my_endpoint(request: MyRequest) -> MyResponse:
    """Endpoint description."""
    # Implementation
    return MyResponse(...)
```

2. **Register router** in `app/main.py`:

```python
from app.routers import my_feature

app.include_router(my_feature.router)
```

3. **Add tests** for the new endpoint

### Adding a New Service

1. **Create service file** (e.g., `app/services/my_service.py`):

```python
import logging

logger = logging.getLogger(__name__)

class MyService:
    """Service description."""
    
    def __init__(self):
        logger.info("MyService initialized")
    
    def do_something(self, param: str) -> str:
        """Method description."""
        # Implementation
        return result

# Global instance
my_service = MyService()
```

2. **Export service** in `app/services/__init__.py`:

```python
from app.services.my_service import my_service

__all__ = [..., "my_service"]
```

3. **Use in routers**:

```python
from app.services import my_service

@router.post("/")
async def my_endpoint():
    result = my_service.do_something("param")
    return {"result": result}
```

### Adding a New Consent Type

1. **Update enum** in `app/models/schemas.py`:

```python
class ConsentType(str, Enum):
    WELLNESS_GUIDANCE = "wellness_guidance"
    MY_NEW_TYPE = "my_new_type"
```

2. **Enforce consent** in protected endpoints:

```python
from app.services import consent_manager
from app.models.schemas import ConsentType

# At the start of your endpoint
if not consent_manager.verify_or_deny(user_id, ConsentType.MY_NEW_TYPE):
    raise HTTPException(
        status_code=403,
        detail="Consent required for this operation"
    )
```

3. **Document the consent purpose** in API docs

### Adding New Pydantic Models

1. **Define models** in `app/models/schemas.py`:

```python
class MyRequest(BaseModel):
    """Request description."""
    field: str = Field(..., description="Field description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "field": "example value"
            }
        }

class MyResponse(BaseModel):
    """Response description."""
    result: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

2. **Export models** in `app/models/__init__.py`

## Testing

### Manual Testing

Use the included test script:

```bash
python test_api.py
```

### Testing Individual Endpoints

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Grant consent
curl -X POST http://localhost:8000/api/v1/consent/grant \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "consent_type": "wellness_guidance", "purpose": "Testing"}'

# Get guidance
curl -X POST http://localhost:8000/api/v1/wellness/guidance \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "query": "Test question"}'
```

## Documentation

When adding features:

1. **Update README.md** with new usage examples
2. **Add docstrings** to all public functions/classes
3. **Update ARCHITECTURE.md** if adding new components
4. **Include examples** in Pydantic model schemas

## Consent Implementation Checklist

For any endpoint that processes user data or performs AI computation:

- [ ] Add consent type to `ConsentType` enum
- [ ] Call `verify_or_deny()` before computation
- [ ] Return 403 if consent is denied
- [ ] Log consent decisions
- [ ] Document consent purpose
- [ ] Include consent status in response
- [ ] Test consent grant/deny workflow

## Privacy Checklist

- [ ] Minimize data collection
- [ ] Never log sensitive user data
- [ ] Use local processing (no external APIs)
- [ ] Implement consent verification
- [ ] Support consent revocation
- [ ] Document data usage clearly
- [ ] Provide transparency to users

## Pull Request Process

1. **Create a feature branch**: `git checkout -b feature/my-feature`
2. **Make your changes** following the guidelines above
3. **Test thoroughly**: Ensure all endpoints work correctly
4. **Update documentation**: README, ARCHITECTURE, docstrings
5. **Commit with clear messages**: Describe what and why
6. **Push and create PR**: Provide detailed description

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Changes Made
- List of specific changes

## Testing Done
- How you tested the changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Added/updated documentation
- [ ] Privacy principles maintained
- [ ] Consent enforcement verified (if applicable)
- [ ] Manual testing completed
```

## Common Patterns

### Error Handling

```python
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

@router.post("/")
async def my_endpoint():
    try:
        # Your logic here
        return result
    except SpecificError as e:
        logger.error(f"Specific error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User-friendly error message"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# Info: Normal operations
logger.info(f"Processing request for user={user_id}")

# Warning: Potential issues
logger.warning(f"Consent not found for user={user_id}")

# Error: Errors that need attention
logger.error(f"Failed to process: {error}")

# Never log sensitive data!
# ❌ logger.info(f"Password: {password}")
# ✅ logger.info(f"User authenticated: {user_id}")
```

## Questions or Issues?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide detailed information and steps to reproduce

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to S.O.F.I.E.! 🌟
