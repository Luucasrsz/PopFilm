FROM python:3.9.15-slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .  

RUN pip install -r requirements.txt  

ADD ./web .  

EXPOSE 8080
CMD ["python", "back-end/python/app.py", "runserver"]

