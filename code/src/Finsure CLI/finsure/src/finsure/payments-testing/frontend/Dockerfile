# Use official Python image as a base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy frontend source code
COPY ./src /app/src
COPY ./backend/src /app/backend/src

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to include backend source
ENV PYTHONPATH="/app/backend/src"


# Run Streamlit server
CMD ["streamlit", "run",  "/app/src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
