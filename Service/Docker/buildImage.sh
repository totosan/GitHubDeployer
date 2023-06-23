docker build . -f ./Service/Docker/Dockerfile.net -t totosan/deployerservice:latest
docker push totosan/deployerservice:latest