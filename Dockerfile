FROM python:3.9-slim

RUN pip install flask

WORKDIR /app

COPY app/ /app/

EXPOSE 8080

CMD ["python", "server.py"]

