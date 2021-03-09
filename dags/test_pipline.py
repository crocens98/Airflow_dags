from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


def print_hello():
  return 'Hello Wolrd'

dag = DAG('hello_world',
          description='Hello world example',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20),
          catchup=False)

bash_task_first = BashOperator(
    task_id="bash_task_1",
    bash_command='echo "Hello World 1"',
    dag=dag
)

bash_task_second = BashOperator(
    task_id="bash_task_2",
    bash_command='echo "Hello World 2"',
    dag=dag
)

bash_task_first >> bash_task_second
