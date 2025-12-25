FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Create a default .env file if it doesn't exist
RUN touch .env

EXPOSE 8000

CMD ["uvicorn", "api.py:app", "--host", "0.0.0.0", "--port", "8000"]