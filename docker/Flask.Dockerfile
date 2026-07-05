# Use a lightweight Python image
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask requests gunicorn

# Copy the Flask AI app
COPY docker/ai_service.py /app/ai_service.py

# Expose the port Django will reach us on
EXPOSE 5001

# Run with gunicorn for production readiness. 
# Increased timeout to 180s because LLMs can take a while to generate responses.
CMD ["gunicorn", "--timeout", "300", "--bind", "0.0.0.0:5001", "ai_service:app"]
