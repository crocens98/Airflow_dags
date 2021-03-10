# Create Secret with the help of Kubectl
kubectl create secret generic \
  airflow-git-keys \
  --from-file=id_rsa=$HOME/.ssh/id_rsa \
  --from-file=id_rsa.pub=$HOME/.ssh/id_rsa.pub \
  --from-file=known_hosts=$HOME/.ssh/known_hosts \
  --namespace default



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
  
  
# Create user
airflow users create \
          --username admin \
          --firstname Viktar \
          --lastname Zinkou \
          --role Admin \
          --email viktar_zinkou@epam.com \
          --password admin 


# You will see
   export POD_NAME=$(kubectl get pods --namespace default -l "component=web,app=airflow" -o jsonpath="{.items[0].metadata.name}")
   echo http://127.0.0.1:8080
   kubectl port-forward --namespace default $POD_NAME 8081:8080




# Copy from local to kub airflow
kubectl cp /mnt/d/bigdata/task9_scheduling/SparkApp/target/SparkApp-1.0-SNAPSHOT.jar $POD_NAME:/opt/airflow -c airflow-web

kubectl cp /mnt/d/bigdata/task9_scheduling/SparkApp/target/SparkApp-1.0-SNAPSHOT.jar airflow-worker-0:/opt/airflow -c airflow-worker

kubectl exec \
  -it \
   airflow-worker-0 \
  /bin/bash


docker cp /mnt/d/bigdata/task9_scheduling/SparkApp/target/SparkApp-1.0-SNAPSHOT.jar hadoop-container:/
spark-submit --master spark://hadoop-network:7077 --class by.zinkov.App --packages io.delta:delta-core_2.12:0.7.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 --total-executor-cores 4 --executor-cores 2 --executor-memory 2g --driver-memory 2g --name spark_task /SparkApp-1.0-SNAPSHOT.jar


spark-submit --master yarn --class by.zinkov.App --packages io.delta:delta-core_2.12:0.7.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 --total-executor-cores 4 --executor-cores 2 --executor-memory 2g --driver-memory 2g --name spark_task /SparkApp-1.0-SNAPSHOT.jar

spark-submit --master local[1] --class by.zinkov.App --packages io.delta:delta-core_2.12:0.7.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 --total-executor-cores 4 --executor-cores 2 --executor-memory 2g --driver-memory 2g --name spark_task /SparkApp-1.0-SNAPSHOT.jar
