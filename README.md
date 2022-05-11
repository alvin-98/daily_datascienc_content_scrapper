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

## Fact and dimension tables

### Twitter Tables
tweets (fact table):	tweetId, tweetDate, userId,	conversationId,	retweetedTweet, quotedTweet, inReplyToTweetId, mentionedUsers, hashtags, place
twitter_users (dimension table): userId, username, displayname,	description, profileCreated, followersCount, friendsCount, statusesCount, favouritesCount, listedCount,  mediaCount, location, linkUrl
tweet_stats (dimension table): tweetId, replyCount, retweetCount, likeCount, quoteCount
tweet_content (dimension table): tweetId, content, language, outlinks, media, hashtags, url
tweet_time (dimension table): tweetDate, hour, day, week, month, year, weekday

### Youtube Video Tables
youtube_videos (fact table): videoId, publishedAt, channelId
youtube_video_content (dimension table): videoId, title, description,	duration,	dimension, definition, caption,	licensedContent, contentRating,	projection
youtube_video_statistics (dimension table): videoId, viewCount, likeCount, favoriteCount, commentCount
youtube_channel (dimension table): channelId, channelTitle, channelDescription, channelCreatedOn, channelTopicCategories, channelViewCount, channelSubscriberCount, channelHiddenSubscriberCount, channelVideoCount
youtube_videos_time (dimension table): publishedAt, hour, day, week, month, year, weekday


