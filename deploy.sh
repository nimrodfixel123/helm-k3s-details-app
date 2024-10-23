#!/bin/bash

NAMESPACE="default"
RELEASE_NAME="details-app-release"
CHART_DIR="./details-app"

# Check if Helm is installed
if ! command -v helm &> /dev/null
then
    echo "Helm could not be found. Please install Helm and try again."
    exit 1
fi

# Deploy the Helm chart
echo "Deploying the Helm chart..."
helm upgrade --install $RELEASE_NAME $CHART_DIR --namespace $NAMESPACE

# Check if the deployment was successful
if [ $? -eq 0 ]; then
    echo "Deployment successful!"
    echo "App should be available shortly."
else
    echo "Deployment failed!"
    exit 1
fi

# Wait for the services to be up and running
kubectl get pods --namespace $NAMESPACE -w

# Display the NodePort where the app can be accessed
NODE_PORT=$(kubectl get svc --namespace $NAMESPACE details-app -o jsonpath='{.spec.ports[0].nodePort}')
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
echo "You can access the app at http://$NODE_IP:$NODE_PORT"
