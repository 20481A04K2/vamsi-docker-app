# Use an official Python base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy code to the container
COPY . .

# Install Flask
RUN pip install flask

# Expose the port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
