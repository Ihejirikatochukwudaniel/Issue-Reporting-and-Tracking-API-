# Issue Tracker API

A RESTful API for managing and tracking issues built with FastAPI and SQLAlchemy.

## Features

- ✅ Create, Read, Update, Delete (CRUD) operations for issues
- ✅ Issue status tracking (Open, In Progress, Resolved, Closed)
- ✅ Priority levels (Low, Medium, High, Critical)
- ✅ Filtering and pagination support
- ✅ Automatic API documentation (Swagger UI)
- ✅ Input validation with Pydantic
- ✅ SQLite database (easy setup, no external dependencies)




<img width="1350" height="684" alt="swagger tracker 1" src="https://github.com/user-attachments/assets/9e88f723-26ee-4ab2-ac96-289f00801936" />




<img width="1351" height="688" alt="swagger tracker 2" src="https://github.com/user-attachments/assets/40dcad1c-76de-44ec-b5e5-d03acc17fe30" />



## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or create the project directory:**
```bash
mkdir issue-tracker
cd issue-tracker
```

2. **Create a virtual environment (recommended):**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### Accessing the Documentation

- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc (Alternative):** http://localhost:8000/redoc
- **Root Endpoint:** http://localhost:8000/

## API Endpoints

### Create an Issue
```bash
POST /issues/
Content-Type: application/json

{
  "title": "Login button not working",
  "description": "When users click login, nothing happens",
  "status": "open",
  "priority": "high",
  "reporter": "john@example.com",
  "assignee": "jane@example.com"
}
```

### List All Issues
```bash
GET /issues/
# With filters:
GET /issues/?status=open&priority=high&skip=0&limit=10
```

### Get Specific Issue
```bash
GET /issues/1
```

### Update Issue (Full Update)
```bash
PUT /issues/1
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "medium",
  "reporter": "john@example.com",
  "assignee": "jane@example.com"
}
```

### Partial Update
```bash
PATCH /issues/1
Content-Type: application/json

{
  "status": "resolved"
}
```

### Delete Issue
```bash
DELETE /issues/1
```

## Testing with cURL

### Create an issue:
```bash
curl -X POST "http://localhost:8000/issues/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Database connection error",
    "description": "Cannot connect to production database",
    "status": "open",
    "priority": "critical",
    "reporter": "admin@example.com"
  }'
```

### List issues:
```bash
curl "http://localhost:8000/issues/"
```

### Get specific issue:
```bash
curl "http://localhost:8000/issues/1"
```

### Update issue status:
```bash
curl -X PATCH "http://localhost:8000/issues/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

## Project Structure

```
issue-tracker/
├── app/
│   ├── __init__.py          # Makes app a package
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database connection and session management
│   ├── models.py            # SQLAlchemy database models (tables)
│   ├── schemas.py           # Pydantic models for request/response validation
│   └── routes/
│       ├── __init__.py      # Makes routes a package
│       └── issues.py        # Issue-related API endpoints
├── requirements.txt         # Python dependencies
├── issues.db               # SQLite database (created automatically)
└── README.md               # This file
```

## Environment Variables (Optional)

Create a `.env` file in the root directory:

```
DATABASE_URL=sqlite:///./issues.db
API_HOST=0.0.0.0
API_PORT=8000
```

## Deployment Options

### 1. Deploy to Render (Free Tier)

1. Create a `render.yaml`:
```yaml
services:
  - type: web
    name: issue-tracker-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Push to GitHub
3. Connect to Render and deploy

### 2. Deploy to Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

### 3. Deploy to Fly.io

1. Install Fly CLI
2. Create `fly.toml`
3. Run: `fly launch`

### 4. Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t issue-tracker .
docker run -p 8000:8000 issue-tracker
```

## Development Tips

### Enable Auto-reload
The `--reload` flag automatically restarts the server when code changes:
```bash
uvicorn app.main:app --reload
```

### View Database Contents
Use any SQLite viewer or command-line:
```bash
sqlite3 issues.db
.tables
SELECT * FROM issues;
```

### Add More Fields
1. Update `models.py` (add column to Issue model)
2. Update `schemas.py` (add field to Pydantic models)
3. Delete `issues.db` to recreate with new schema
4. Restart the application

## Common Interview Questions & Answers

### Q: Why use FastAPI over Flask?
**A:** FastAPI provides:
- Automatic API documentation (Swagger/OpenAPI)
- Built-in data validation with Pydantic
- Async support out of the box
- Better performance (faster than Flask)
- Type hints support for better IDE experience

### Q: What is the purpose of Pydantic schemas?
**A:** Pydantic schemas:
- Validate incoming data automatically
- Provide clear API contracts
- Separate API models from database models
- Enable automatic API documentation
- Type conversion and validation

### Q: Why separate models.py and schemas.py?
**A:** Separation of concerns:
- `models.py`: Database structure (how data is stored)
- `schemas.py`: API interface (how data is exchanged)
- Allows changing one without affecting the other
- Database might have fields we don't expose via API
- API might accept fields not stored in database

### Q: What is SQLAlchemy ORM?
**A:** ORM (Object-Relational Mapping):
- Write Python code instead of SQL
- Database-agnostic (easily switch databases)
- Prevents SQL injection
- Provides relationships and eager loading
- Type-safe database operations

### Q: How would you add authentication?
**A:** Several approaches:
1. JWT tokens with OAuth2
2. API keys
3. Session-based auth
4. Use libraries like `python-jose`, `passlib`
5. Add `users` table and login endpoint

### Q: How to handle database migrations?
**A:** Use Alembic:
```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Q: How would you add testing?
**A:** Use pytest:
```python
# test_issues.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_issue():
    response = client.post("/issues/", json={
        "title": "Test Issue",
        "reporter": "test@example.com"
    })
    assert response.status_code == 201
```

## Next Steps / Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement comments on issues
- [ ] Add file attachments
- [ ] Email notifications
- [ ] Search functionality
- [ ] Audit logs
- [ ] Rate limiting
- [ ] Caching with Redis
- [ ] Background tasks with Celery
- [ ] WebSocket support for real-time updates

## License

MIT License - Feel free to use this project for learning and development.

## Support


For questions or issues, please open an issue on GitHub or contact the maintainer.
