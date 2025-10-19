FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY deployment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Set environment
ENV PYTHONPATH="/app"

# Expose port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "deployment.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]
