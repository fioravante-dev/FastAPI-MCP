FROM python:3.11

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"
# --- NEW: Set a cache directory INSIDE the image ---
ENV HF_HOME="/app/huggingface_cache"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- NEW: Pre-download the model during the build ---
# Create a small script to import the model, which triggers the download.
# The downloaded files will be stored in the HF_HOME cache directory
# and will be part of the final Docker image layer.
RUN python -c "from llama_index.embeddings.huggingface import HuggingFaceEmbedding; HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')"

# Copy the rest of the project files
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]