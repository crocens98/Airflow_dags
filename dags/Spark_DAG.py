from datetime import datetime, timedelta
from airflow.models import Variable
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks.ssh_hook import SSHHook
password_variable = 'SSH_PASSWORD'
default_args = {
  'owner': 'crocens98',
  'depends_on_past': False,
  'start_date': datetime(2021, 3, 8),
  'retries': 2,
  'retry_delay': timedelta(minutes=5)
}

dag = DAG('spark_airflow',
          default_args=default_args,
          description='Spark work airflow',
          start_date=datetime(2021, 3, 8),
          catchup=False,
          )

bash_task_first = BashOperator(
    task_id="before_spark",
    bash_command='echo "Before Spark"',
    dag=dag
)
sshHook = SSHHook(ssh_conn_id ='ssh_connection')

password = Variable.get(password_variable)
spark_task = SSHOperator(
    task_id='spark_task',
    ssh_hook=sshHook,
    command=f'''docker exec  hadoop-container /root/hadoop/spark-2.4.7-bin-hadoop2.7/bin/spark-submit \
    --master spark://hadoop-host:7077 \
    --deploy-mode cluster \
    --class by.zinkov.App \
    --packages org.apache.spark:spark-avro_2.11:2.4.4 \
    --total-executor-cores 4 \
    --executor-cores 2 \
    --executor-memory 2g \
    --driver-memory 2g \
    --name spark_task \
    /SparkApp-1.0-SNAPSHOT.jar
     ''',
    dag=dag,
)


bash_task_second = BashOperator(
    task_id="after_spark",
    bash_command='echo "After Spark"',
    dag=dag
)


bash_task_first >> spark_task
spark_task >> bash_task_second


