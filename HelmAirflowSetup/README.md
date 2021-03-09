
# Deploy
helm install \
 "airflow" \
 airflow-stable/airflow \
 --version "7.16.0" \
 --namespace "default" \
 --values ./values.yaml



# Connect
kubectl exec \
  -it \
  --namespace "default" \
  --container airflow-web \
  Deployment/airflow-web \
  /bin/bash


# You will see
   export POD_NAME=$(kubectl get pods --namespace default -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}")
   echo http://127.0.0.1:8080
   kubectl port-forward --namespace default $POD_NAME 8080:8080

# Create Secret with the help of Kubectl
kubectl create secret generic \
  airflow-git-keys \
  --from-file=id_rsa=$HOME/.ssh/id_rsa \
  --from-file=id_rsa.pub=$HOME/.ssh/id_rsa.pub \
  --from-file=known_hosts=$HOME/.ssh/known_hosts \
  --namespace default



# Copy from local to kub airflow
kubectl cp /mnt/d/bigdata/task9_scheduling/SparkApp/target/SparkApp-1.0-SNAPSHOT.jar $POD_NAME:/opt/airflow -c airflow-web

