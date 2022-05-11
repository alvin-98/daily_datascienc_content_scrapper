import snscrape.snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
import configparser
import boto3
from google_api_python_client.googleapiclient.discovery import build
from airflow.contrib.hooks.aws_hook import AwsHook


today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")
limit = 10

AWS_ACCESS_KEY = config['AWS']['aws_access_key']
AWS_SECRET_KEY = config['AWS']['aws_secret_key']


s3 = boto3.client('s3', region_name='us-east-1', 
                         aws_access_key_id=AWS_ACCESS_KEY, 
                         aws_secret_access_key=AWS_SECRET_KEY)


def extract_tweets():
    query = f'("data OR science" OR "machine OR learning" OR "meta OR analysis" OR "ai OR research" OR "data OR engineering" OR  "data OR analysis" OR "visualization") until:{today} since:{yesterday}'
    tweets = []
    

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():

        if len(tweets) == limit:
            break

        else:
            #tweet details
            url = tweet.url
            tweetDate = tweet.date
            content = tweet.content
            tweetId = tweet.id
            replyCount = tweet.replyCount
            retweetCount = tweet.retweetCount
            likeCount = tweet.likeCount
            quoteCount = tweet.quoteCount
            conversationId = tweet.conversationId
            language = tweet.lang
            outlinks = tweet.outlinks
            media = tweet.media
            retweetedTweet = tweet.retweetedTweet
            quotedTweet = tweet.quotedTweet
            inReplyToTweetId = tweet.inReplyToTweetId
            mentionedUsers = tweet.mentionedUsers
            hashtags = tweet.hashtags
            place = tweet.place

            #user details
            userId = tweet.user.id
            username = tweet.user.username
            displayname = tweet.user.displayname
            description = tweet.user.description
            descriptionUrls = tweet.user.descriptionUrls
            profileCreated = tweet.user.created
            followersCount = tweet.user.followersCount
            friendsCount = tweet.user.friendsCount
            statusesCount = tweet.user.statusesCount
            favouritesCount = tweet.user.favouritesCount
            listedCount = tweet.user.listedCount
            mediaCount = tweet.user.mediaCount
            location = tweet.user.location
            linkUrl = tweet.user.linkUrl


            tweets.append([url,
                         tweetDate, # unix epoch timestamp in milliseconds
                         content,
                         tweetId,
                         replyCount,
                         retweetCount,
                         likeCount,
                         quoteCount,
                         conversationId,
                         language,
                         outlinks,
                         media,
                         retweetedTweet,
                         quotedTweet,
                         inReplyToTweetId,
                         mentionedUsers,
                         hashtags,
                         place,
                         userId,
                         username,
                         displayname,
                         description,
                         descriptionUrls,
                         profileCreated,
                         followersCount,
                         friendsCount,
                         statusesCount,
                         favouritesCount,
                         listedCount,
                         mediaCount,
                         location,
                         linkUrl])

    tweets_df = pd.DataFrame(tweets, columns=['url',
                         'tweetDate',
                         'content',
                         'tweetId',
                         'replyCount',
                         'retweetCount',
                         'likeCount',
                         'quoteCount',
                         'conversationId',
                         'language',
                         'outlinks',
                         'media',
                         'retweetedTweet',
                         'quotedTweet',
                         'inReplyToTweetId',
                         'mentionedUsers',
                         'hashtags',
                         'place',
                         'userId',
                         'username',
                         'displayname',
                         'description',
                         'descriptionUrls',
                         'profileCreated',
                         'followersCount',
                         'friendsCount',
                         'statusesCount',
                         'favouritesCount',
                         'listedCount',
                         'mediaCount',
                         'location',
                         'linkUrl'])


    twitter_data_filename = f'twitter_extract_{datetime.now().strftime("%Y_%m_%d_%H_%M")}.json'
    tweets_df.to_json(twitter_data_filename)

    s3.upload_file(Bucket='dsc-staging',
               Filename=twitter_data_filename, 
               Key=f'tweet_data/{twitter_data_filename}')


    
def extract_youtubevideos():
    config = configparser.ConfigParser()
    config.read('config.cfg')

    youtube_query = '"data science" | "machine learning" | "meta analysis" | "ai research" | "data engineering" | "data analysis" | "visualization"'

    with build('youtube', 'v3', developerKey=config['YOUTUBE']['api_key']) as service:
        request = service.search().list(
            part='snippet',
            maxResults=10,
            q=youtube_query,
            type='video',
            publishedAfter=f"{yesterday}T00:00:00Z",
            publishedBefore=f"{today}T00:00:00Z",
        )
        response = request.execute()



    youtube_videos = []
    for item in response['items']:
        
        try:
            videoId = item['id']['videoId']
        except KeyError:
            videoId = None
        
        try:
            publishedAt = item['snippet']['publishedAt']
            publishedAt = publishedAt.replace('T', ' ')
            publishedAt = publishedAt[:-1]
        except KeyError:
            publishedAt = None
            
        try:
            channelId = item['snippet']['channelId']
        except KeyError:
            channelId = None
            
        try:
            title = item['snippet']['title']
        except KeyError:
            title = None
            
        try:
            channelTitle = item['snippet']['channelTitle']
        except KeyError:
            channelTitle = None

        youtube_videos.append([videoId,
                              publishedAt,
                              channelId,
                              title,
                              channelTitle])


    video_df = pd.DataFrame(youtube_videos, columns=['videoId', 'publishedAt', 'channelId', 'title', 'channelTitle'])


    with build('youtube', 'v3', developerKey=config['YOUTUBE']['api_key']) as service:
        request = service.videos().list(
            part='snippet, statistics, contentDetails',
            maxResults=1,
            id=video_df['videoId'].tolist()
        )
        response = request.execute()

    videoDetailsList = []    
    for item in response['items']:
        
        
        try:
            videoId = item['id']
        except KeyError:
            videoId = None

        try:
            description = item['snippet']['description']
        except KeyError:
            description = None
            
        try:
            duration = item['contentDetails']['duration']
        except KeyError:
            duration = None
            
        try:
            dimension = item['contentDetails']['dimension']
        except KeyError:
            dimension = None
            
        try:
            definition = item['contentDetails']['definition']
        except KeyError:
            definition = None
            
        try:
            caption = item['contentDetails']['caption']
        except KeyError:
            caption = None
            
        try:
            licensedContent = item['contentDetails']['licensedContent']
        except KeyError:
            licensedContent = None
            
        try:
            contentRating = item['contentDetails']['contentRating']
        except KeyError:
            contentRating = None
            
        try:
            projection = item['contentDetails']['projection']
        except KeyError:
            projection = None

        try:
            viewCount = item['statistics']['viewCount']
        except KeyError:
            viewCount = None
            
        try:
            likeCount = item['statistics']['likeCount']
        except KeyError:
            likeCount = None
            
        try:
            favoriteCount = item['statistics']['favoriteCount']
        except KeyError:    
            favoriteCount = None
            
        try:
            commentCount = item['statistics']['commentCount']
        except KeyError:
            commentCount = None

        videoDetailsList.append([videoId,
                                description,
                                duration,
                                dimension,
                                definition,
                                caption,
                                licensedContent,
                                contentRating,
                                projection,
                                viewCount,
                                likeCount,
                                favoriteCount,
                                commentCount])

    video_df2 = pd.DataFrame(videoDetailsList, columns=['videoId',
                                'description',
                                'duration',
                                'dimension',
                                'definition',
                                'caption',
                                'licensedContent',
                                'contentRating',
                                'projection',
                                'viewCount',
                                'likeCount',
                                'favoriteCount',
                                'commentCount'])

    video_df12 = pd.merge(video_df, video_df2, on='videoId')

    with build('youtube', 'v3', developerKey=config['YOUTUBE']['api_key']) as service:
        request = service.channels().list(
            part='snippet,statistics,topicDetails,id',
            # maxResults=1,
            id=df['channelId'].tolist()
        )
        response=request.execute()
        
        
    channelDetailsList = []   
    for item in response['items']:

        try:
            channelId = item['id']
        except KeyError:
            channelId = None

        try:
            channelDescription = item['snippet']['description']
        except KeyError:
            channelDescription = None 

        try:
            channelCreatedOn = item['snippet']['publishedAt']
            channelCreatedOn = channelCreatedOn.replace('T', ' ')
            channelCreatedOn = channelCreatedOn[:-1]
        except KeyError:
            channelCreatedOn = None 

        try:
            channelTopicCategories = item['topicDetails']['topicCategories']
        except KeyError:
            channelTopicCategories = None
        
        try:
            channelViewCount = item['statistics']['viewCount']
        except KeyError:
            channelViewCount = None 

        try:
            channelSubscriberCount = item['statistics']['subscriberCount']
        except KeyError:
            channelSubscriberCount = None 
        
        try:
            channelHiddenSubscriberCount = item['statistics']['hiddenSubscriberCount']
        except KeyError:
            channelHiddenSubscriberCount = None 

        try:
            channelVideoCount = item['statistics']['videoCount']
        except KeyError:
            channelVideoCount = None
        
        channelDetailsList.append([channelId,
                                   channelDescription,
                                   channelCreatedOn,
                                   channelTopicCategories,
                                   channelViewCount,
                                   channelSubscriberCount,
                                   channelHiddenSubscriberCount,
                                   channelVideoCount])
        
    video_df3 = pd.DataFrame(channelDetailsList, columns=['channelId',
                                                    'channelDescription',
                                                    'channelCreatedOn',
                                                    'channelTopicCategories',
                                                    'channelViewCount',
                                                    'channelSubscriberCount',
                                                    'channelHiddenSubscriberCount',
                                                    'channelVideoCount'])

    youtube_df = pd.merge(video_df12, video_df3, on='channelId')

    youtube_data_filename = f'youtube_extract_{datetime.now().strftime("%Y_%m_%d_%H_%M")}.json'
    youtube_df.to_json(youtube_data_filename)

    
    s3.upload_file(Bucket='dsc-staging',
               Filename=youtube_data_filename, 
               Key=f'youtubevideos_data/{youtube_data_filename}')


    
if __name__ == '__main__':
    
    extract_youtubevideos()
    extract_tweets()
    
    print('extracted socials')