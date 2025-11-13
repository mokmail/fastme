FROM python:3.12-slim-trixie AS base

# Copy uv binaries from Astral’s prebuilt uv image into /bin/
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files from the current directory to /app in the container
COPY . /app

# Optional: Print the path to uv and its version for debugging
RUN which uv && uv --version

# Install dependencies using uv, respecting the lock file
RUN uv sync --locked

# Expose port 7860 for external access

# Run the Gradio app using uv


# Expose the port the app will run on
EXPOSE 80

# Start Uvicorn; adjust "main:app" to the module:path of your FastAPI app if different
CMD [ "uv", "run", "app.py", "--host", "0.0.0.0", "--port", "80"]