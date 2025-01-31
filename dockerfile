FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "run.py"]