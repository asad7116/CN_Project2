# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code to the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the application
CMD [ "python", "app.py" ]
