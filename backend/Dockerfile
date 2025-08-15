# Stage 1: Build the virtual environment with dependencies
FROM python:3.12 as builder

# Install uv, our package manager, globally in the builder image
RUN pip install uv

# Create a virtual environment in a standard location
RUN uv venv /opt/venv

# Explicitly activate the virtual environment for subsequent RUN commands
# by setting the VIRTUAL_ENV environment variable.
ENV VIRTUAL_ENV=/opt/venv

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies using the global 'uv', which will now respect
# the VIRTUAL_ENV and install packages into /opt/venv.
RUN uv pip install --no-cache-dir -r requirements.txt


# Stage 2: Create the final, lean production image
FROM python:3.12-slim

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Add the virtual environment's bin directory to the PATH
# This allows running 'uvicorn' directly
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy the application source code into the working directory
COPY main.py .
COPY tree_engine.py .
COPY firebase_setup.py .

# --- IMPORTANT SECURITY NOTE ---
# DO NOT copy the 'firebase-credentials.json' file into the Docker image.
# In a real-world deployment on Google Cloud Run, you should store the
# content of this JSON file in Google Secret Manager and mount it as a
# secret volume or environment variable during runtime.
# The 'firebase_setup.py' would then need to be adapted to read from
# that secret instead of a file.

# Expose the port that the application will run on
EXPOSE 8000

# Define the command to run the application
# We use Uvicorn, a fast ASGI server.
# --host 0.0.0.0 makes the server accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
