FROM python:3.10-slim

WORKDIR /app

# Copy dependency definition and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app code and serialized model
COPY app.py .
COPY superkart_model.joblib .

# Expose Flask default port
EXPOSE 5000

# Start Flask application
CMD ["python", "app.py"]