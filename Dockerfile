FROM python:3.9.15-slim

#prueba
RUN mkdir /app
WORKDIR /app

#copy
COPY requirements.txt .  

RUN pip install -r requirements.txt  

ADD ./web .  

EXPOSE 8080
CMD ["python", "python/app.py", "runserver"]

