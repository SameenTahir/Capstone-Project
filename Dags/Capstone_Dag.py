from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2020, 1, 10),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('Capstone_Final_Project_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

Load_Immig_Data_into_Redshift = StageToRedshiftOperator(
    task_id='Immigration_Data',
    dag=dag,
    table="Immigration_Data_stg",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-capstone",
    s3_key="immigration_data",
    data_path="s3://udacity-capstone/immigration_data.csv"
)

Load_Airport_Data_into_Redshift = StageToRedshiftOperator(
    task_id='Airport_codes',
    dag=dag,
    table="Airport_codes_Stg",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-capstone",
    s3_key="Airport_codes",
	data_path="s3://udacity-capstone/airport_codes.csv"

)

load_fact_immigration_table = LoadFactOperator(
    task_id='load_fact_immigration_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="fact_immigration_data",
    select_query=SqlQueries.immigration_data_insert
)

load_airportcodes_dimension_table = LoadDimensionOperator(
    task_id='Load_airport_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="dim_airport_codes",
    truncate_table=True,
    select_query=SqlQueries.airport_codes_table_insert
)

load_visatype_dimension_table = LoadDimensionOperator(
    task_id='Load_visatype_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="songs",
    truncate_table=True,
    select_query=SqlQueries.visatype_table_insert
)

load_date_hierarchy_dimension_table = LoadDimensionOperator(
    task_id='Load_date_hierarchy_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="artists",
    truncate_table=True,
    select_query=SqlQueries.date_hierarchy_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=[
        "songplays",
        "users",
        "songs",
        "artists",
        "time"],
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

## Stage-1 ##
start_operator >> Load_Immig_Data_into_Redshift
start_operator >> Load_Airport_Data_into_Redshift

## Stage-2 ##
Load_Airport_Data_into_Redshift >> load_fact_immigration_table
Load_Airport_Data_into_Redshift >> load_airportcodes_dimension_table
Load_Airport_Data_into_Redshift >> load_visatype_dimension_table
Load_Airport_Data_into_Redshift >> load_date_hierarchy_dimension_table

## Stage-3 ##
load_fact_immigration_table >> run_quality_checks
load_airportcodes_dimension_table >> run_quality_checks
load_visatype_dimension_table >> run_quality_checks
load_date_hierarchy_dimension_table >> run_quality_checks

## Stage-4 ##
run_quality_checks >> end_operator
