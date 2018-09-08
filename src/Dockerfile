FROM debian:buster

LABEL maintainer=<joppich@bricknet.de>

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -yq && \
    apt-get install -yq --no-install-recommends \
        python3 python3-pip python3-setuptools \
        sqlite3 python3-dev pandoc && \
    rm -r /var/lib/apt/lists /var/cache/apt/*

ENV LANG C.UTF-8  
ENV LC_ALL C.UTF-8

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN useradd -md /srv/brickwall runner -u 1000 && \
    mkdir -p /srv/data/db && mkdir /srv/data/content && \
    chown -R runner:runner /srv/data

WORKDIR /srv/brickwall
USER runner

ADD . .
EXPOSE 5000

ENTRYPOINT ["/srv/brickwall/docker-entrypoint.sh"]

CMD "default"
