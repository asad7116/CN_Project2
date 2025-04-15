# Use the official Python slim image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY app.py .

# Expose port 5000 for the Flask server
EXPOSE 5000

# Run the application when the container starts
CMD ["python", "app.py"]
