FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY model ./model

# Environment variables
ENV MODEL_PATH=/app/model/saved_model_iris.pkl

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]
