# Dockerfile (FINAL, PRODUCTION VERSION)

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- THE KEY FIX IS HERE ---
# Copy the ENTIRE project context (including the 'app' sub-directory)
# from your local machine into the container's working directory.
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your app using uvicorn.
# This now works because the 'app' package is a subdirectory of our WORKDIR.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]