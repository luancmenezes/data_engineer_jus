FROM python:3.6-alpine

RUN apk update
RUN apk add --no-cache pcre-dev python3-dev libffi libffi-dev libxslt-dev libressl-dev
RUN apk add --no-cache --virtual build-dependencies git g++ gcc libc-dev linux-headers build-base musl-dev

COPY . /var/www
WORKDIR /var/www

RUN pip3 install -r /var/www/requirements.txt
RUN rm -r /tmp/ && rm -rf /var/cache/apk/* && apk del build-dependencies

EXPOSE 80 9200

CMD ["/usr/local/bin/uwsgi", "--ini", "/var/www/uwsgi.ini"]

