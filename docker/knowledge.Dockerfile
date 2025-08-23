FROM python:3.11-slim
WORKDIR /app
COPY services/knowledge /app
RUN pip install fastapi uvicorn
CMD ["python", "src/knowledge/api/main.py"]
