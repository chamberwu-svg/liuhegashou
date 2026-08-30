FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY ai-lottery-lab/frontend/package*.json ./
RUN npm install
COPY ai-lottery-lab/frontend ./
RUN npm run build

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY ai-lottery-lab/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai-lottery-lab/backend /app/backend
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

ENV PYTHONPATH=/app/backend
ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

