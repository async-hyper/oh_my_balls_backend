# Balls Game API

A simple backend API project built with FastAPI.

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Project

```bash
# Method 1: Using uvicorn command
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Method 2: Run main.py directly
python main.py
```

## API Endpoints

- `GET /` - Hello World endpoint
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation (auto-generated)

## Access API

After starting, you can access through the following addresses:

- API base address: http://localhost:8000
- Swagger documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Test API

```bash
# Test Hello World endpoint
curl http://localhost:8000/

# Test health check endpoint
curl http://localhost:8000/health
```



