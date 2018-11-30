FROM alpine:3.8

RUN apk update && \
    apk upgrade && \
    apk --no-cache add --update \
        wget \
        ca-certificates \
        openssl \
        tzdata \
        curl \
        bash \
        bash-completion \
        tar \
        unzip \
        jq \
        git \
        openssh-client \
        less \
        netcat-openbsd

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.4.0/wait /usr/local/bin/waitforsvcs
RUN chmod +x /usr/local/bin/waitforsvcs && \
    ln -s /usr/local/bin/waitforsvcs /usr/local/bin/wait-for-svc-connections

## wait wrapper for easy entrypoint/command setup
COPY ./waitthendo.sh /usr/local/bin/waitthendo
