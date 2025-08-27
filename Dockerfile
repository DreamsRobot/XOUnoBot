FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Environment variables (optional)
# ENV API_ID=...
# ENV API_HASH=...
# ENV BOT_TOKEN=...
# ENV MONGO_URL=...

# Start bot
CMD ["python", "main.py"]
