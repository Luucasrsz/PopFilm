FROM python:3.9.15-slim

RUN mkdir /app
WORKDIR /app

# 🔹 Copiar requirements.txt primero
COPY requirements.txt .  

# 🔹 Instalar dependencias antes de copiar el resto del código
RUN pip install -r requirements.txt  

# 🔹 Ahora copiar el código fuente
COPY ./web .  

EXPOSE 8080
CMD ["python", "back-end/python/app.py", "runserver"]

