FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install .
CMD ["infra-agent", "--help"]
