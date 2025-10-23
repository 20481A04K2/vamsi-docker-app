FROM python:3.9-slim


# Set the working directory in the container
WORKDIR /app


# Install dependencies directly
# We install 'flask' which is required for app.py
RUN pip install --no-cache-dir flask firebase-admin


# Copy the Flask application code into the container
COPY app.py .
COPY index.html .


# Expose the port the app runs on
EXPOSE 5000


# Set the command to run the application
# We use 'python app.py' to execute the main block in your script
CMD ["python", "app.py"]

