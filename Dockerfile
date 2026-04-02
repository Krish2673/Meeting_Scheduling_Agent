# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (HF Spaces expects this)
EXPOSE 7860

# Run server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]