FROM python:3.11-slim
WORKDIR /app
COPY services/browser-pool /app
RUN pip install fastapi uvicorn
CMD ["python", "src/browser_pool/healthcheck.py"]
