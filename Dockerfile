# Use the official NVIDIA PyTorch base image
FROM pytorch/pytorch:2.12.1-cuda13.2-cudnn9-devel


# Set the working directory inside the container
WORKDIR /workspace

# (Optional) Install any additional python packages you need
# COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages fastapi[standard] uvicorn easyocr sqlalchemy "psycopg[binary,pool]"

# Keep the container alive or run your script
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

