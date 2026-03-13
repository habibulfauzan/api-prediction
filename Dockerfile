FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app", "--workers", "1", "--threads", "4", "--timeout", "120"]

