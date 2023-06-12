FROM python:3.11.4-alpine3.18

COPY templates /templates
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .

ENTRYPOINT ["/usr/local/bin/python", "/main.py"]
