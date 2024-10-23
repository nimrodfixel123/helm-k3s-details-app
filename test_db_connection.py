import os
import time
import requests
import subprocess

# Kubernetes-specific variables
APP_URL = 'http://details-app.local/api/health_check'  # The app's service URL in Kubernetes
DB_POD_LABEL = 'app=postgres-container'  # Label to identify the PostgreSQL pod
DB_NAMESPACE = 'default'  # Namespace where the PostgreSQL pod is running (update if necessary)

def check_app_connection():
    """
    Check if the application is running and can connect to the database.
    """
    try:
        response = requests.get(APP_URL, timeout=5)
        if response.status_code == 200:
            print("Application is connected to the database.")
            return True
        else:
            print(f"Application error: Status Code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False

def restart_db_pod():
    """
    Attempt to restart the PostgreSQL pod in Kubernetes.
    """
    print(f"Restarting PostgreSQL pod with label: {DB_POD_LABEL}")
    try:
        # Find the pod name using the label selector
        pod_name = subprocess.check_output(
            ["kubectl", "get", "pods", "-l", DB_POD_LABEL, "-n", DB_NAMESPACE, "-o", "jsonpath={.items[0].metadata.name}"]
        ).decode('utf-8').strip()

        if pod_name:
            # Delete the pod to restart it (Kubernetes will recreate the pod automatically)
            subprocess.run(["kubectl", "delete", "pod", pod_name, "-n", DB_NAMESPACE], check=True)
            print(f"Pod {pod_name} restarted successfully.")
        else:
            print(f"No pod found with label {DB_POD_LABEL}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart database pod: {e}")
    except Exception as e:
        print(f"Error finding pod: {e}")

def verify_and_fix_connection():
    """
    Verify the application is connected to the database. If not, try to restart the DB pod and retry.
    """
    if not check_app_connection():
        print("Attempting to fix the issue by restarting the database pod.")
        restart_db_pod()

        # Wait a few seconds for the pod to restart
        time.sleep(20)

        # Recheck the connection
        if check_app_connection():
            print("Connection fixed and application is now connected to the database.")
        else:
            print("The issue persists. Please check the application logs for further investigation.")
    else:
        print("No issues detected.")

if __name__ == "__main__":
    print("Starting application and database connection test...")
    verify_and_fix_connection()
