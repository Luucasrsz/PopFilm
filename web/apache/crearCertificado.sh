#Ejecuta el siguiente comando para generar la clave privada (server.key):
openssl genrsa -out server.key 2048
# A continuación, ejecuta el siguiente comando para generar la solicitud de firma de certificado (CSR).
# Te pedirá que proporciones información como el nombre del país, la organización, etc. 
openssl req -new -key server.key -out server.csr
# A continuación, ejecuta el siguiente comando para generar un certificado autofirmado (server.crt) utilizando la clave privada y el CSR
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
# Esto generará un certificado autofirmado válido por 365 días y lo guardará en un archivo llamado "server.crt"