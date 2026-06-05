FROM python:3.12-slim

WORKDIR /app

# Le requirements.txt est dans utils/
COPY utils/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
