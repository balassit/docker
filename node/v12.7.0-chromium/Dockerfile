FROM node:12.7.0-alpine
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
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.1/wait /usr/local/bin/waitforit
RUN chmod +x /usr/local/bin/waitforit

# Install Chromium, Xvfb
RUN apk add --update --no-cache\
    udev\
    ttf-freefont\
    chromium-chromedriver=72.0.3626.121-r0\
    chromium=72.0.3626.121-r0 \
    shadow

ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/

CMD ["sh"]
