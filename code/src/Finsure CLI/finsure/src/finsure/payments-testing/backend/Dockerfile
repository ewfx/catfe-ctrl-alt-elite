# Use official Python image as a base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy backend source code
COPY ./src /app/src

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to allow imports
# ENV PYTHONPATH=/app/backend/src
ENV PYTHONPATH="/app/src"

# Expose API port
EXPOSE 8000
EXPOSE 8001

# Run FastAPI server
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
