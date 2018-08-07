Docker build and run

```
CGO_ENABLED=0 GOOS=linux go build -a -x -o main .
docker build -t test -f Dockerfile .
docker run -it test
```

## Deploy to ECR
```
aws ecr create-repository --repository-name test
aws ecr get-login --no-include-email --region us-west-2
docker tag test:latest 541362214851.dkr.ecr.us-west-2.amazonaws.com/test:latest
docker push 541362214851.dkr.ecr.us-west-2.amazonaws.com/test:latest
```

## Deploy to ECS
```
aws ecs register-task-definition --cli-input-json file://test-task-def.json
aws ecs run-task --task-definition test
```
