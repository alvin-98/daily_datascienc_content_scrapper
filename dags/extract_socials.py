import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
import boto3
from airflow.models import Variable
from googleapiclient.discovery import build
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook

today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")


AWS_KEY = AwsBaseHook('aws_credentials', client_type='s3').get_credentials().access_key
AWS_SECRET = AwsBaseHook('aws_credentials', client_type='s3').get_credentials().secret_key

YOUTUBE_API_KEY = Variable.get('youtube_api_key')

s3 = boto3.client('s3', region_name='us-east-1', 
                         aws_access_key_id=AWS_KEY, 
                         aws_secret_access_key=AWS_SECRET)


def extract_tweets():
    
    query = f'("data science" OR "machine learning" OR "meta analysis" OR "ai research" OR "data engineering" OR  "data analysis" OR "data visualization") until:{today} since:{yesterday}'
    tweets = []
    
    limit = 1000
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():

        if len(tweets) == limit:
            break

        else:
            #tweet details
            try:
                url = tweet.url
            except AttributeError:
                print('AttributeError @url')
                url = None
            
            try:
                tweetDate = tweet.date
            except AttributeError:
                print('AttributeError @tweetDate')
                tweetDate = None 

            try:
                content = tweet.content
            except AttributeError:
                print('AttributeError @content')
                content = None 

            try:
                tweetId = str(tweet.id)
            except AttributeError:
                print('AttributeError @id')
                tweetId = None 

            try:
                replyCount = int(tweet.replyCount)
            except AttributeError:
                print('AttributeError @replyCount')
                replyCount = None 

            try:
                retweetCount = int(tweet.retweetCount)
            except AttributeError:
                print('AttributeError @retweetCount')
                retweetCount = None 

            try:
                likeCount = int(tweet.likeCount)
            except AttributeError:
                print('AttributeError @likeCount')
                likeCount = None 

            try:
                quoteCount = int(tweet.quoteCount)
            except AttributeError:
                print('AttributeError @quoteCount')
                quoteCount = None 

            try:
                conversationId = str(tweet.conversationId)
            except AttributeError:
                print('AttributeError @conversationId')
                conversationId = None 

            try:
                language = tweet.lang
            except AttributeError:
                print('AttributeError @language')
                language = None 

            try:
                outlinks = tweet.outlinks
            except AttributeError:
                print('AttributeError @outlinks')
                outlinks = None 

            try:
                media = tweet.media
            except AttributeError:
                print('AttributeError @media')
                media = None 

            try:
                retweetedTweet = str(tweet.retweetedTweet.id)
            except AttributeError:
                print('AttributeError @retweetedTweet')
                retweetedTweet = None 
            
            try:
                quotedTweet = str(tweet.quotedTweet.id)
            except AttributeError:
                print('AttributeError @quotedTweet')
                quotedTweet = None 

            try: 
                inReplyToTweetId = str(tweet.inReplyToTweetId)
            except AttributeError:
                print('AttributeError @inReplyToTweetId')
                inReplyToTweetId = None 

            try:
                mentionedUsers = tweet.mentionedUsers
            except AttributeError:
                print('AttributeError @mentionedUsers')
                mentionedUsers = None 

            try:
                hashtags = tweet.hashtags
            except AttributeError:
                print('AttributeError @hashtags')
                hashtags = None 

            try:
                place = tweet.place
            except AttributeError:
                print('AttributeError @place')
                place = None 

            #user details

            try:
                userId = str(tweet.user.id)
            except AttributeError:
                print('AttributeError @userid')
                userId = None 

            try: 
                username = tweet.user.username
            except AttributeError:
                print('AttributeError @username')
                username = None 

            try:
                displayname = tweet.user.displayname
            except AttributeError:
                print('AttributeError @displayname')
                displayname = None 

            try:
                description = tweet.user.description
            except AttributeError:
                print('AttributeError @userDescription')
                description = None 

            try:
                descriptionUrls = tweet.user.descriptionUrls
            except AttributeError:
                print('AttributeError @descriptionUrls')
                descriptionUrls = None 

            try: 
                profileCreated = tweet.user.created
            except AttributeError:
                print('AttributeError @profileCreated')
                profileCreated = None 

            try: 
                followersCount = int(tweet.user.followersCount)
            except AttributeError:
                print('AttributeError @followersCount')
                followersCount = None 

            try:
                friendsCount = int(tweet.user.friendsCount)
            except AttributeError:
                print('AttributeError @friendsCount')
                friendsCount = None 

            try:
                statusesCount = int(tweet.user.statusesCount)
            except AttributeError:
                print('AttributeError @statusesCount')
                statusesCount = None 

            try:
                favouritesCount = int(tweet.user.favouritesCount)
            except AttributeError:
                print('AttributeError @favoritesCount')
                favouritesCount = None 

            try:
                listedCount = int(tweet.user.listedCount)
            except AttributeError:
                print('AttributeError @listedCount')
                listedCount = None 

            try:
                mediaCount = int(tweet.user.mediaCount)
            except AttributeError:
                print('AttributeError @mediaCount')
                mediaCount = None 

            try:
                location = tweet.user.location
            except AttributeError:
                print('AttributeError @location')
                location = None 
            
            try:  
                linkUrl = tweet.user.linkUrl
            except AttributeError:
                print('AttributeError @linkUrl')
                linkUrl = None 


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
                        retweetedTweet,
                        quotedTweet,
                        inReplyToTweetId,
                        userId,
                        username,
                        displayname,
                        description,
                        followersCount,
                        friendsCount,
                        statusesCount,
                        favouritesCount,
                        listedCount,
                        mediaCount])

    tweets_df = pd.DataFrame(tweets, columns=['url',
                        'tweet_date',
                        'content',
                        'tweet_id',
                        'reply_count',
                        'retweet_count',
                        'like_count',
                        'quote_count',
                        'conversation_id',
                        'language',
                        'retweeted_tweet_id',
                        'quoted_tweet_id',
                        'inreply_to_tweet_id',
                        'user_id',
                        'username',
                        'displayname',
                        'description',
                        'followers_count',
                        'friends_count',
                        'statuses_count',
                        'favourites_count',
                        'listed_count',
                        'media_count'])


    for i in tweets_df.index:
        twitter_data_filename = f'twitter_extract_T{today}_Y{yesterday}_N{datetime.now().strftime(f"%Y_%m_%d_%H_%M_%S")}_R{i}.json'
        tweets_df.loc[i].to_json(twitter_data_filename, date_format='epoch', date_unit='s')
        
        s3.upload_file(Bucket='datascience-content-staging',
                   Filename=twitter_data_filename, 
                   Key=f'tweet_data/{twitter_data_filename}')

    
def extract_youtubevideos():

    youtube_query = '"data science" | "machine learning" | "meta analysis" | "ai research" | "data engineering" | "data analysis" | "data visualization"'

    with build('youtube', 'v3', developerKey=YOUTUBE_API_KEY) as service:
        request = service.search().list(
            part='snippet',
            maxResults=100,
            q=youtube_query,
            type='video',
            publishedAfter=f"{yesterday}T00:00:00Z",
            publishedBefore=f"{today}T00:00:00Z",
        )
        response = request.execute()



    youtube_videos = []
    for item in response['items']:
        
        try:
            videoId = str(item['id']['videoId'])
        except KeyError:
            print('KeyError @videoid')
            videoId = None
        
        try:
            publishedAt = item['snippet']['publishedAt']
        except KeyError:
            print('KeyError @publishedAt')
            publishedAt = None
            
        try:
            channelId = str(item['snippet']['channelId'])
        except KeyError:
            print('KeyError @channelId')
            channelId = None
            
        try:
            title = item['snippet']['title']
        except KeyError:
            print('KeyError @title')
            title = None
            
        try:
            channelTitle = item['snippet']['channelTitle']
        except KeyError:
            print('KeyError @channelTitle')
            channelTitle = None

        youtube_videos.append([videoId,
                              publishedAt,
                              channelId,
                              title,
                              channelTitle])


    video_df = pd.DataFrame(youtube_videos, columns=['video_id', 'published_at', 'channel_id', 'title', 'channel_title'])


    with build('youtube', 'v3', developerKey=YOUTUBE_API_KEY) as service:
        request = service.videos().list(
            part='snippet, statistics, contentDetails',
            # maxResults=1,
            id=video_df['video_id'].tolist()
        )
        response = request.execute()

    videoDetailsList = []    
    for item in response['items']:
        
        
        try:
            videoId = str(item['id'])
        except KeyError:
            print('KeyError @videoid2')
            videoId = None

        try:
            description = item['snippet']['description']
        except KeyError:
            print('KeyError @description')
            description = None
            
        try:
            duration = item['contentDetails']['duration']
        except KeyError:
            print('KeyError @duration')
            duration = None
            
        try:
            dimension = item['contentDetails']['dimension']
        except KeyError:
            print('KeyError @dimension')
            dimension = None
            
        try:
            definition = item['contentDetails']['definition']
        except KeyError:
            print('KeyError @definition')
            definition = None
            
        try:
            caption = item['contentDetails']['caption']
        except KeyError:
            print('KeyError @caption')
            caption = None
            
        try:
            licensedContent = str(item['contentDetails']['licensedContent'])
        except KeyError:
            print('KeyError @licensedContent')
            licensedContent = None
            
        try:
            contentRating = item['contentDetails']['contentRating']
        except KeyError:
            print('KeyError @contentRating')
            contentRating = None
            
        try:
            projection = item['contentDetails']['projection']
        except KeyError:
            print('KeyError @projection')
            projection = None

        try:
            viewCount = int(item['statistics']['viewCount'])
        except KeyError:
            print('KeyError @viewCount')
            viewCount = None
            
        try:
            likeCount = int(item['statistics']['likeCount'])
        except KeyError:
            print('KeyError @likeCount')
            likeCount = None
            
        try:
            favoriteCount = int(item['statistics']['favoriteCount'])
        except KeyError:    
            print('KeyError @favouritesCount')
            favoriteCount = None
            
        try:
            commentCount = int(item['statistics']['commentCount'])
        except KeyError:
            print('KeyError @commentCount')
            commentCount = None

        videoDetailsList.append([videoId,
                                description,
                                duration,
                                dimension,
                                definition,
                                caption,
                                licensedContent,
                                projection,
                                viewCount,
                                likeCount,
                                favoriteCount,
                                commentCount])

    video_df2 = pd.DataFrame(videoDetailsList, columns=['video_id',
                                'description',
                                'duration',
                                'dimension',
                                'definition',
                                'caption',
                                'licensed_content',
                                'projection',
                                'view_count',
                                'like_count',
                                'favorite_count',
                                'comment_count'])

    video_df12 = pd.merge(video_df, video_df2, on='video_id')

    with build('youtube', 'v3', developerKey=YOUTUBE_API_KEY) as service:
        request = service.channels().list(
            part='snippet,statistics,topicDetails,id',
            # maxResults=1,
            id=video_df12['channel_id'].tolist()
        )
        response=request.execute()
        
        
    channelDetailsList = []   
    for item in response['items']:

        try:
            channelId = str(item['id'])
        except KeyError:
            print('KeyError @channelId')
            channelId = None

        try:
            channelDescription = item['snippet']['description']
        except KeyError:
            print('KeyError @channelDescription')
            channelDescription = None 

        try:
            channelCreatedOn = item['snippet']['publishedAt']
        except KeyError:
            print('KeyError @channelCreatedOn')
            channelCreatedOn = None 

        try:
            channelTopicCategories = item['topicDetails']['topicCategories']
        except KeyError:
            print('KeyError @channelTopicCategories')
            channelTopicCategories = None
        
        try:
            channelViewCount = int(item['statistics']['viewCount'])
        except KeyError:
            print('KeyError @channelViewCount')
            channelViewCount = None 

        try:
            channelSubscriberCount = int(item['statistics']['subscriberCount'])
        except KeyError:
            print('KeyError @channelSubscriberCount')
            channelSubscriberCount = None 
        
        try:
            channelHiddenSubscriberCount = str(item['statistics']['hiddenSubscriberCount'])
        except KeyError:
            print('KeyError @channelHiddenSubscriberCount')
            channelHiddenSubscriberCount = None 

        try:
            channelVideoCount = int(item['statistics']['videoCount'])
        except KeyError:
            print('KeyError @channelViewCount')
            channelVideoCount = None
        
        channelDetailsList.append([channelId,
                                   channelDescription,
                                   channelViewCount,
                                   channelSubscriberCount,
                                   channelHiddenSubscriberCount,
                                   channelVideoCount])
        
    video_df3 = pd.DataFrame(channelDetailsList, columns=['channel_id',
                                                    'channel_description',
                                                    'channel_view_count',
                                                    'channel_subscriber_count',
                                                    'channel_hidden_subscriber_count',
                                                    'channel_video_count'])

    youtube_df = pd.merge(video_df12, video_df3, on='channel_id')
    youtube_df['published_at'] = pd.to_datetime(youtube_df['published_at'], infer_datetime_format=True)


    for i in youtube_df.index:
        youtube_data_filename = f'youtube_extract_T{today}_Y{yesterday}_N{datetime.now().strftime(f"%Y_%m_%d_%H_%M_%S")}_R{i}.json'
        youtube_df.loc[i].to_json(youtube_data_filename, date_format='epoch', date_unit='s')
        

        s3.upload_file(Bucket='datascience-content-staging',
                   Filename=youtube_data_filename, 
                   Key=f'youtubevideos_data/{youtube_data_filename}')

    
if __name__ == '__main__':
    
    extract_youtubevideos()
    extract_tweets()
    
    print('extracted socials')