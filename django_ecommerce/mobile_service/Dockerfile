FROM python:3.9-slim

# Install build dependencies
RUN apt-get update && apt-get install -y gcc make pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8012

CMD ["python", "manage.py", "runserver", "0.0.0.0:8012"]