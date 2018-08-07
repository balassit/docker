```
CGO_ENABLED=0 GOOS=linux go build -a -x -o main .
docker build -t example-scratch -f Dockerfile .
docker run -it example-scratch
```
