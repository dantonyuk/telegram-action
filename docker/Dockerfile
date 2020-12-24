FROM python:3.8.7-alpine3.12

COPY templates /templates
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .

ENTRYPOINT ["/usr/local/bin/python", "/main.py"]
