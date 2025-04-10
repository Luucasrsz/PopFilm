FROM ubuntu:20.04
ENV APACHE_USER_DATA=www-data
ENV APACHE_GROUP_DATA=www-data

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y apache2
RUN apt install -y libapache2-mod-security2 openssl

# Configuracion basica
COPY apache2.conf /etc/apache2/apache2.conf
COPY ports.conf /etc/apache2/ports.conf
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./static/ /usr/local/apache2/htdocs/
RUN chown -R www-data:www-data /usr/local/apache2/htdocs && chmod -R 755 /usr/local/apache2/htdocs


# Habilitar https
COPY ./default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
COPY ./server.crt /etc/ssl/certs/server.crt
COPY ./server.key /etc/ssl/private/server.key
COPY ./pass.sh /etc/ssl/private/pass.sh
RUN chmod u+x /etc/ssl/private/pass.sh
RUN a2enmod ssl
RUN a2ensite default-ssl

# Habilitar mod-security
RUN a2enmod security2
COPY modsecurity.conf /etc/modsecurity/modsecurity.conf
RUN mkdir /etc/apache2/modsecurity-crs/
COPY coreruleset-3.3.0/ /etc/apache2/modsecurity-crs/
COPY coreruleset-3.3.0/crs-setup.conf /etc/modsecurity/crs


# Habilitar mod-evasive
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install libapache2-mod-evasive
COPY evasive.conf /etc/apache2/mods-enabled/evasive.conf
RUN mkdir /var/log/mod_evasive && chown www-data:www-data /var/log/mod_evasive

#Habilitar proxy
RUN a2enmod proxy proxy_http

#Seguridad avanzada
RUN a2enmod headers rewrite
COPY security.conf /etc/apache2/conf-available/security.conf
RUN a2dismod userdir status
#RUN a2dismod alias
#RUN a2dismod autoindex

# Reiniciar apache2
RUN service apache2 stop
RUN service apache2 start

EXPOSE 80
EXPOSE 443
CMD ["apachectl", "-D", "FOREGROUND"]
