from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import \
  SparkSubmitOperator

spark_jars_home = '/opt/airflow'
spark_app_jar = 'SparkApp-1.0-SNAPSHOT.jar'

default_args = {
  'owner': 'crocens98',
  'depends_on_past': False,
  'start_date': datetime(2021, 3, 8, tzinfo=local_tz),
  'email': ['crocens98@gmail.com'],
  'email_on_failure': True,
  'email_on_retry': True,
  'retries': 2,
  'retry_delay': timedelta(minutes=5)
}

dag = DAG('spark_airflow',
          default_args=default_args,
          description='Spark work airflow',
          start_date=datetime(2021, 3, 8),
          catchup=False,
          )

flight_search_ingestion = SparkSubmitOperator(task_id='spark_task',
                                              conn_id='spark_connection',
                                              application=f'{spark_jars_home}/{spark_app_jar}',
                                              jar_class='by.zinkov.App',
                                              total_executor_cores=4,
                                              packages="io.delta:delta-core_2.12:0.7.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0",
                                              executor_cores=2,
                                              executor_memory='2g',
                                              driver_memory='2g',
                                              name='spark_task',
                                              execution_timeout=timedelta(
                                                  minutes=10),
                                              dag=dag
                                              )
