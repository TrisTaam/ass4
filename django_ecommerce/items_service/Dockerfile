FROM python:3.9-slim
RUN apt-get update && apt-get install -y gcc make && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8005
CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]