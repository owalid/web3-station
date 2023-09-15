FROM python:3.11.4-bookworm

WORKDIR /root

COPY challenges ./challenges
COPY challenges.yaml .
COPY main.py .
COPY requirements.txt .
COPY .env .
COPY py_server ./py_server

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "main.py"]
