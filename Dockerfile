FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 7860

CMD ["sh", "-c", "python -m uvicorn server.app:app --host 0.0.0.0 --port ${PORT:-7860}"]