import os
def cargarvariables():
    os.environ['DB_USERNAME']='root'
    os.environ['DB_PASSWORD']='example'
    os.environ['DB_DATABASE']='POPFILM'
    os.environ['DB_HOST']='localhost'
    os.environ['DB_PORT']='3306'
    os.environ['PORT']='8080'
    os.environ['HOST']='0.0.0.0'
    
# 🔹 Clave secreta para JWT (Cámbiala en producción y usa variables de entorno)
    os.environ['JWT_SECRET_KEY'] = 'lucaselpelucas'  
