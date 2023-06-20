docker build . -f ./Docker/Dockerfile.net -t totosan/deployerservice:latest
docker push totosan/deployerservice:latest