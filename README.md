# Data Science Content Scrapper

## Overview
There are numerous resource to learn and keep updated with the rapid developments in AI. Many professionals in the domain post their experiences, learnings, and achievements on Twitter, in addition to this there are educational videos, research paper discussions, conference speeches, etc available on Youtube. This project to collect daily material from these two sources and store them in Redshift. The data can further be processed and served in numerous ways and can also be used for analysis. Some of the potential applications are listed below:
1. Analysis of top content of the day and comparison between the two platforms
2. Text summarization to create a digestible summary of the days' happenings
3. Curation of top tweets and Youtube videos
4. Personal recommendation of relevant content based on notes taken

## Method
1. The data is scrapped from Youtube using its API, while snscrape is used to extract tweets from Twitter.
2. The search API from both these sources are utilized and additional methods are called based on requirement.
3. The data is then stored in json format. Json was chosen (as opposed to columnar storage such as parquet) so as to retain maximum flexibility for analysis and tasks like applying NLP on text data.
4. The Json files are then stored in S3 object store. As the data will grow over time, S3 will provide a scalable and cost effective storage for storing extracted data. We can hence, pull in data from S3 directly to other data warehouses or relational databases for separate processing whenever required.
5. Next, we move the data from S3 to Staging tables in Redshift, before moving data into fact and dimension tables. This step was done with daily top content analysis in mind; with data in fact and dimension tables, we can easily query to perform any analysis required. 
6. This whole process is designed to be run automatically and thus Airflow is used for orchestration. 
7. The facts and dimension tables are designed to facilitate multiple analysis (in relation to users, content, time of posting, etc). 

## Performance under alternate scenarios
1. The data was increased 100x
- The S3 store and Redshift are scalable as the requirements increases, however, there will be a cost incurred based the data stored and time for which the clusters have to run. Therefore, it is better to create and shutdown Redshift clusters after usage.
- The current setup brings in 1 million tweets and 10 thousand youtube videos every day and the Redshift facts and dimension tables are truncated every time before loading in data.

2. The database needs to be accessed by 100+ people
- The extraction part of the pipeline can be turned into an API for anyone to use, perhaps using a service like AWS Lambda.
- In an organisation environment, the Redshift database can be accessed by providing access using IAM access controls.
- Redshift has a concurrency scaling option using which virtually facilitates unlimited concurrent users and concurrent queries with fast performance.

## Note
1. Add in your Youtube API key and AWS credentials to the config file 
2. Create an S3 bucket 'dsc-staging' and folders named 'youtubevideos_data' and 'tweet_data' to store data from these two sources respectively
3. Spin up a Redshift cluster and add a connection named 'redshift' using airflow ui

## Fact and dimension tables (Data Dictionary)

#### Tweets Table (Facts Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
tweet_id | text | 260 bytes | PRIMARY KEY | unique id assigned by twitter to each tweet |
tweet_date | timestamp | precision upto seconds | NOT NULL | date & time when the tweet was posted |
user_id | text | 260 bytes | NOT NULL | unique id assigned to by twitter to each user |
conversation_id | text | 260 bytes | - | unique id assigned to each conversation by twitter |
retweeted_tweet_id | varchar(max) | 65535 bytes | - | tweet_id of a retweeted tweet |
quoted_tweet_id | varchar(max) | 65535 bytes | - | tweet_id of a quoted tweet |
inreply_to_tweet_id | varchar(max) | 65535 bytes | - | tweet_id of the replied tweet |

#### Twitter Users Table (Dimension Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
user_id | text | 260 bytes | PRIMARY KEY | unique id assigned to by twitter to each user |
username | text | 260 bytes | - | username associated with user_id |
displayname | text | 260 bytes | - | displayname associate with user_id |
description | varchar(max) | 65535 bytes | - | description provided by user |
followers_count | int8 | 8 bytes | - | number of followers of user |
friends_count | int8 | 8 bytes | - | number of friends added by the user |
statuses_count | int8 | 8 bytes | - | number of statuses posted by the user |
favourites_count | int8 | 8 bytes | - | number of tweets saved in favourites by user |
listed_count | int8 | 8 bytes | - | number of people who have added user to their list |
media_count | int8 | 8 bytes | - | number of media items posted by user |

#### Tweet Stats Table (Dimension Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
tweet_id | text | 260 bytes | PRIMARY KEY | unique id assigned by twitter to each tweet |
reply_count | int8 | 8 bytes | - | number of replies to the tweet |
retweet_count | int8 | 8 bytes | - | number of times tweet has been retweeted |
like_count | int8 | 8 bytes | - | number of times tweet was liked |
quote_count | int8 | 8 bytes | - | number of times tweet has been quoted |

#### Tweet Content Table (Dimension Table) 
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
tweet_id | text | 260 bytes | PRIMARY KEY | unique id assigned by twitter to each tweet |
content | varchar(max) | 65535 bytes | NOT NULL | content of the tweet |
language | varchar(10) | 10 bytes | - | language of tweet |
url | varchar(max) | 65535 bytes | - | url of tweet |

#### Tweet Time Table (Dimension Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
tweet_date | timestamp | precision upto seconds | NOT NULL | date & time when the tweet was posted |
hour | int8 | 8 bytes | - | hour when tweet was posted |
day | int8 | 8 bytes | - | day of month when tweet was posted |
week | int8 | 8 bytes | - | week when tweet was posted |
month | varchar(256) | 256 bytes | - | month when tweet was posted |
year | int8 | 8 bytes | 8 bytes | - | year when tweet was posted |
weekday | varchar(256) | 256 bytes | - | day of week when tweet was posted |

#### Youtube Videos Table (Facts Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
video_id | text | 260 bytes | PRIMARY KEY | unique id assigned by Youtube to the video |
published_at | timestamp | precision upto seconds | NOT NULL | date & time when the video was posted |
channel_id | text | 260 bytes | NOT NULL | unique id of channel assigned by Youtube that posted the video |

#### Youtube Video Content Table (Dimension Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
video_id | text | 260 bytes | PRIMARY KEY | unique id assigned by Youtube to the video |
title | text | 260 bytes | NOT NULL | title of the video |
description | text | 260 bytes | - | description of the video |
duration | varchar(20) | 20 bytes | - | duration of video in minutes (number following 'M') and seconds (number following 'S') | 
definition | varchar(10) | 10 bytes | - | video quality, whether high definition or standard definition | 
caption | varchar(10) | 10 bytes | - | whether captions are available for the video |
liscensed_content | varchar(10) | 10 bytes | - | Whether content was uploaded to channel linked to YouTube content partner and claimed by partner |
projection | varchar(20) | 20 bytes | - | projection format, whether 360 or rectangular video |


#### Youtube Video Statistics Table (Dimension Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
video_id | text | 260 bytes | PRIMARY KEY | unique id assigned by Youtube to the video |
view_count | int8 | 8 bytes | - | views on the video |
like_count | int8 | 8 bytes | - | likes on the video |
favourite_count | int8 | 8 bytes | - | number of times video has been added to favourites |
comment_count | int8 | 8 bytes | - | number of comments on the video |

#### Youtube Channel Table (Dimension Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
channel_id | text | 260 bytes | PRIMARY KEY | unique id of channel assigned by Youtube that posted the video |
channel_title | text | 260 bytes | NOT NULL | title of the channel |
channel_description | varchar(max) | 65535 bytes | - | description of the channel |
channel_view_count | int8 | 8 bytes | - | number of views on the channel |
channel_subscriber_count | int8 | 8 bytes | - | number of subscribers to the channel |
channel_hidden_subscriber_count | int8 | 8 bytes | - | whether the channel has hid its subscriber count |
channel_video_count | int8 | 8 bytes | - | number of videos posted by channel |

#### Youtube Videos Time Table (Dimension Table)
Field Name | Datatype | FieldLength | Constraint | Description | 
--- | --- | --- | --- |--- |
published_at | timestamp | precision upto seconds | NOT NULL | date & time when the video was posted |
hour | int8 | 8 bytes | - | hour when video was posted |
day | int8 | 8 bytes | - | day of month when video was posted |
week | int8 | 8 bytes | - | week when video was posted |
month | varchar(256) | 256 bytes | - | month when video was posted |
year | int8 | 8 bytes | 8 bytes | - | year when video was posted |
weekday | varchar(256) | 256 bytes | - | day of week when video was posted |
 


### Relationships between the data tables



## Sample Query

The table schema was designed to make it effiecient to extract and serve tweet content and use additional filters, based on popularity and time period, if needed to serve best tweets.

- Query to extract the top tweets shared in the data science domain in the past month
```
SELECT distinct twt.tweet_id, tc.url, tc.content, ts.retweet_count, ts.like_count
FROM ((tweets AS twt 
JOIN tweet_content AS tc 
ON twt.tweet_id = tc.tweet_id)
JOIN tweet_stats AS ts 
ON twt.tweet_id = ts.tweet_id)
WHERE twt.tweet_date > '2022-04-01 00:00:00'      
ORDER BY ts.retweet_count DESC
LIMIT 10
```
Result (partial image as too large to take a single screenshot on redshift):


### A look at the amount of data in tables

Below is the result of the following query to look at the number of rows in tables-
```
select tab.table_schema,
       tab.table_name,
       tinf.tbl_rows as rows
from svv_tables tab
join svv_table_info tinf
          on tab.table_schema = tinf.schema
          and tab.table_name = tinf.table
where tab.table_type = 'BASE TABLE'
      and tab.table_schema not in('pg_catalog','information_schema')
      and tinf.tbl_rows > 1
order by tinf.tbl_rows desc;
```

