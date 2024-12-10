FROM python:3.9.15-slim
RUN mkdir /app
WORKDIR /app
ADD ./web .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py", "runserver"]