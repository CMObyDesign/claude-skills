FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastmcp==3.4.2 uvicorn==0.49.0 requests==2.34.2
EXPOSE 8080
CMD ["python", "server.py"]
