# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Clone Editto repository
RUN git clone https://github.com/EzioBy/Ditto.git /app/ditto

# Install DiffSynth-Studio (as mentioned in Editto docs)
WORKDIR /app/ditto
RUN pip3 install -e .

# Copy our handler script
COPY handler.py /app/handler.py
COPY requirements.txt /app/requirements.txt

# Install additional requirements
RUN pip3 install -r /app/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create directories for models and outputs
RUN mkdir -p /app/models /app/outputs

# Expose port for RunPod handler
EXPOSE 8000

# Run the handler
CMD ["python3", "/app/handler.py"]
