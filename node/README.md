# node-docker
Repository for building node docker images

To build an image, first clone this repo and then refer to sections below for commands to run.

## Latest
Node 10.13.0 with Chromedriver/Chromium.
~~~ bash
cd v10.13.0-chromium
docker build --build-arg http_proxy=$http_proxy -t balassit/node:{YOUR_TAG_HERE} .
~~~
