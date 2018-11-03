FROM python:3.7-alpine3.8
LABEL author="Blake Lassiter<balassit@ncsu.edu>"

RUN apk update && \
    apk upgrade && \
    apk --no-cache add --update \
    wget \
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
    musl-dev \
    openssl-dev \
    gcc \
    libffi-dev \
    shadow \
    zip && \
    rm -rf /var/cache/apk/*

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.4.0/wait /usr/local/bin/wait-for-svc-connections
RUN chmod +x /usr/local/bin/wait-for-svc-connections && \
    ln -s /usr/local/bin/wait-for-svc-connections /usr/local/bin/waitforsvcs

RUN pip3 install virtualenv pipenv
ENV PIPENV_VENV_IN_PROJECT=1

CMD [ "sh" ]