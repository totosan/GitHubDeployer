#az containerapp env create -n deployer -g $RG
tag=$(date '+%y%m%d%H%M')
#tag="latest"
az containerapp create -n deployer-app -g $RG \
            --image totosan/deployerservice \
            --environment deployer \
            --cpu 0.5 --memory 1.0Gi \
            --min-replicas 0 --max-replicas 1 \
            --secrets tokensec=$TOKEN \
            --secrets storage=$AZURE_STORAGE_CONNECTION_STRING \
            --env-vars TOKEN=secretref:tokensec \
            --env-vars AZURE_STORAGE_CONNECTION_STRING=secretref:storage \
            --revision-suffix "deploywatcher-"$tag \
            --ingress external\
            --target-port 8080 