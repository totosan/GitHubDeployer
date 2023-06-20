set -o allexport
source ./Service/src/.env
set +o allexport

#az containerapp env create -n deployer -g $RG --logs-workspace-id 0b4fa5e8-d964-4959-856a-f831e7abc916 --logs-workspace-key oC4u33VXrYH+HusrHU2C34UkKbYrefU73E7P6lQW7dmIQiVMjbKPEmgWu8FVt+P0R64UGq1dEs0N30cUpHzwrw== --logs-workspace-id 0b4fa5e8-d964-4959-856a-f831e7abc916 --logs-destination log-analytics
tag=$(date '+%y%m%d%H%M')
#tag="latest"
az containerapp create -n deployer-app -g $RG \
            --image totosan/deployerservice \
            --environment deployer \
            --cpu 0.5 --memory 1.0Gi \
            --min-replicas 1 \
            --secrets tokensec=$TOKEN storage=$AZURE_STORAGE_CONNECTION_STRING ghappid=$GHAPP_ID ghapp-whsecret=$GHAPP_WEBHOOKSECRET ghapp-pem="$GHAPP_PEMCERTIFICATE" ghapp-installationid=$GHAPP_INST_ID \
            --env-vars TOKEN=secretref:tokensec AZURE_STORAGE_CONNECTION_STRING=secretref:storage GHAPP_ID=secretref:ghappid GHAPP_WEBHOOKSECRET=secretref:ghapp-whsecret GHAPP_PEMCERTIFICATE=secretref:ghapp-pem GHAPP_INST_ID=secretref:ghapp-installationid \
            --revision-suffix "deploywatcher-"$tag \
            --ingress external\
            --target-port 8080 