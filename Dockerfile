FROM python:3.10-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when container starts
CMD ["python", "extract_and_analyze.py"]
