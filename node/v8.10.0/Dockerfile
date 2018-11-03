FROM node:8.10.0-alpine
LABEL author="Blake Lassiter<balassit@ncsu.edu>"

RUN apk update && \
    apk upgrade && \
    apk --no-cache add --update \
        yarn \
        bash \
        git \
        shadow \
        zip && \
    rm -rf /var/cache/apk/*

RUN npm config set registry https://registry.npmjs.org/ && \
    yarn config set registry https://registry.npmjs.org/

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.4.0/wait /usr/local/bin/waitforit
RUN chmod +x /usr/local/bin/waitforit
