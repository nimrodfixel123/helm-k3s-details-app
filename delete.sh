#!/bin/bash

# Define variables
RELEASE_NAME="details-app-release"  # Change this if your release name is different
NAMESPACE="default"

# Uninstall the Helm release
echo "Deleting Helm release..."
helm uninstall $RELEASE_NAME --namespace $NAMESPACE

# Check if the deletion was successful
if [ $? -eq 0 ]; then
    echo "Helm release deleted successfully!"
else
    echo "Failed to delete Helm release!"
    exit 1
fi

# Optional: Delete persistent volume claims (PVCs)
echo "Deleting Persistent Volume Claims (PVCs)..."
kubectl delete pvc --namespace $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME

# Verify deletion
kubectl get all --namespace $NAMESPACE
echo "All resources for the app should be deleted."
