FROM nginx:latest

LABEL maintainer=<joppich@bricknet.de>

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -yq &&\
    rm -r /var/lib/apt/lists /var/cache/apt/*

ADD certs nginx.conf /srv/nginx/
ADD brickwall-ui /srv/nginx/brickwall-ui/

RUN ln -s /srv/nginx/certs/server.crt /etc/nginx/server.crt &&\
    ln -s /srv/nginx/certs/server.key /etc/nginx/server.key &&\
    rm /etc/nginx/nginx.conf &&\
    ln -s /srv/nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm /var/log/nginx/access.log /var/log/nginx/error.log &&\
    ln -s /dev/stdout /var/log/nginx/access.log &&\
    ln -s /dev/stderr /var/log/nginx/error.log

EXPOSE 80
EXPOSE 443


CMD usr/sbin/nginx -g 'daemon off;'
