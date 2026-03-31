FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastmcp uvicorn
EXPOSE 8080
CMD ["python", "server.py"]
