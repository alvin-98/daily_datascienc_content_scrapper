from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
from airflow.operators.dummy_operator import DummyOperator

from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator

from airflow.operators.postgres_operator import PostgresOperator
from helpers import SqlQueries
from airflow.operators.python_operator import PythonOperator

import extract_socials
 
 
AWS_KEY = AwsBaseHook('aws_credentials', client_type='s3').get_credentials().access_key
AWS_SECRET = AwsBaseHook('aws_credentials', client_type='s3').get_credentials().secret_key

TRUNCATE_MODE = True 

default_args = {
    'owner': 'alvinv',
    'start_date': datetime(2022, 5, 7),
    'depends_on_past':False,
    'retries':3,
    'retry_delay':timedelta(minutes=5),
    'catchup':False,
}


dag = DAG('datascience_content_ETL_dag',
          default_args=default_args,
          description='Extract data science content from socials, load and transform data in Redshift with Airflow',
          schedule_interval='@daily'
        )


start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


python_extract_tweets_task = PythonOperator(
    task_id='extract_tweets_to_s3',
    python_callable=extract_socials.extract_tweets,
    dag=dag)


python_extract_youtubevideos_task = PythonOperator(
    task_id='extract_youtubevideos_to_s3',
    python_callable=extract_socials.extract_youtubevideos,
    dag=dag)


create_tables = PostgresOperator(
    task_id='create_tables',
    dag=dag,
    postgres_conn_id='redshift',
    sql=create_tables.sql
)


stage_tweets_to_redshift = StageToRedshiftOperator(
    task_id='Stage_tweets',
    dag=dag,
    redshift_conn_id='redshift',
    table='staging_tweets',
    access_key=AWS_KEY,
    secret_key=AWS_SECRET,
    s3_bucket=Variable.get('dsc_staging_bucket'),
    s3_key='tweet_data',
    region='us-east-1',
    json_path="auto"
)


stage_youtubevideos_to_redshift = StageToRedshiftOperator(
    task_id='Stage_youtubevideos',
    dag=dag,
    redshift_conn_id='redshift',
    table='staging_videos',
    access_key=AWS_KEY,
    secret_key=AWS_SECRET,
    s3_bucket=Variable.get('dsc_staging_bucket'),
    s3_key='youtubevideos_data',
    region='us-east-1',
    json_path="auto"
)


load_tweets_table = LoadFactOperator(
    task_id='Load_tweets_fact_table',
    dag=dag,
    table='tweets',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.tweets_table_insert
)


load_twitter_users_dimension_table = LoadDimensionOperator(
    task_id='Load_twitter_users_dim_table',
    dag=dag,
    table='twitter_users',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.twitter_users_table_insert,
    truncate_mode=TRUNCATE_MODE
)


load_tweet_stats_dimension_table = LoadDimensionOperator(
    task_id='Load_tweet_stats_dim_table',
    dag=dag,
    table='tweet_stats',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.tweet_stats_table_insert,
    truncate_mode=TRUNCATE_MODE
)


load_tweet_content_dimension_table = LoadDimensionOperator(
    task_id='Load_tweet_content_dim_table',
    dag=dag,
    table='tweet_content',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.tweet_content_table_insert,
    truncate_mode=TRUNCATE_MODE
)


load_tweet_time_dimension_table = LoadDimensionOperator(
    task_id='Load_tweet_time_dim_table',
    dag=dag,
    table='tweet_time',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.tweet_time_table_insert,
    truncate_mode=TRUNCATE_MODE
)


load_youtube_videos_table = LoadFactOperator(
    task_id='Load_youtube_videos_fact_table',
    dag=dag,
    table='youtube_videos',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.youtube_videos_table_insert
)


load_youtube_video_content_dimension_table = LoadDimensionOperator(
    task_id='Load_youtube_video_content_dim_table',
    dag=dag,
    table='youtube_video_content',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.youtube_video_content_table_insert,
    truncate_mode=TRUNCATE_MODE
)


load_youtube_video_statistics_dimension_table = LoadDimensionOperator(
    task_id='Load_youtube_video_statistics_dim_table',
    dag=dag,
    table='youtube_video_statistics',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.youtube_video_statistics_table_insert,
    truncate_mode=TRUNCATE_MODE
)


load_youtube_channel_dimension_table = LoadDimensionOperator(
    task_id='Load_youtube_channel_dim_table',
    dag=dag,
    table='youtube_channel',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.youtube_channel_table_insert,
    truncate_mode=TRUNCATE_MODE
)


load_youtube_videos_time_dimension_table = LoadDimensionOperator(
    task_id='Load_youtube_videos_time_dim_table',
    dag=dag,
    table='youtube_videos_time',
    redshift_conn_id='redshift',
    select_stmt=SqlQueries.youtube_videos_time_table_insert,
    truncate_mode=TRUNCATE_MODE
)


run_quality_checks_pkeys = DataQualityOperator(
    task_id='Run_data_quality_checks_pkeys',
    dag=dag,
    qc = [
        {'query':'SELECT COUNT(*) FROM public.tweets WHERE tweet_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.twitter_users WHERE user_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.tweet_stats WHERE tweet_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.tweet_content WHERE tweet_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.tweet_time WHERE tweet_date IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_videos WHERE video_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_video_content WHERE video_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_video_statistics WHERE video_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_channel WHERE channel_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_videos_time WHERE published_at IS NULL','expectation':0},
    ],
    redshift_conn_id='redshift'
)


run_quality_checks_content = DataQualityOperator(
    task_id='Run_data_quality_checks_content',
    dag=dag,
    qc = [
        {'query':'SELECT COUNT(*) FROM public.tweets WHERE user_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.tweets WHERE tweet_date IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.tweet_content WHERE content IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_videos WHERE published_at IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_videos WHERE channel_id IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_video_content WHERE title IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_video_content WHERE duration IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_channel WHERE channel_title IS NULL','expectation':0},
        {'query':'SELECT COUNT(*) FROM public.youtube_videos_time WHERE published_at IS NULL','expectation':0},
    ],
    redshift_conn_id='redshift'
)


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> [python_extract_tweets_task, python_extract_youtubevideos_task] \
               >> create_tables \
               >> [stage_tweets_to_redshift, stage_youtubevideos_to_redshift] \
               >> load_tweets_table \
               >> load_youtube_videos_table \
               >> [load_twitter_users_dimension_table, load_tweet_stats_dimension_table, load_tweet_content_dimension_table, load_tweet_time_dimension_table, load_youtube_video_content_dimension_table, load_youtube_channel_dimension_table, load_youtube_videos_time_dimension_table, load_youtube_video_statistics_dimension_table] \
               >> run_quality_checks_pkeys \
               >> run_quality_checks_content \
               >> end_operator
