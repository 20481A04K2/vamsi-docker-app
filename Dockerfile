# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Copy all files into the container
COPY . .

# Expose the port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
