FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY app ./app

EXPOSE 443
EXPOSE 80

RUN pip install -r requirements.txt

CMD [ "python", "app/main.py" ]