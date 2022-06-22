az containerapp env create -n deployer -g $RG

az containerapp create -n deployer-app -g $RG \
            --image totosan/deployerservice \
            --environment deployer \
            --cpu 0.5 --memory 1.0Gi \
            --min-replicas 1 --max-replicas 1 \
            --secrets tokensec=$TOKEN \
            --env-vars TOKEN=secretref:tokensec \
            --ingress external\
            --target-port 8080 