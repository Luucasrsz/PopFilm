FROM httpd:2.4.33-alpine

RUN apk update && apk upgrade

# Copiar el archivo de configuración de Apache
COPY demo.apache.conf /usr/local/apache2/conf/demo.apache.conf
RUN echo "Include /usr/local/apache2/conf/demo.apache.conf" \
    >> /usr/local/apache2/conf/httpd.conf

# Copiar toda la carpeta static a htdocs
COPY ./static/ /usr/local/apache2/htdocs/
