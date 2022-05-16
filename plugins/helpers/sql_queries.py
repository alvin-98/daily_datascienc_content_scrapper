class SqlQueries:
    tweets_table_insert = ("""
        SELECT distinct tweet_id,
            TIMESTAMP 'epoch' + tweet_date * interval '1 second' as tweet_date,
            user_id,
            conversation_id, 
            retweeted_tweet_id, 
            quoted_tweet_id,
            inreply_to_tweet_id
        FROM staging_tweets
        WHERE tweet_id IS NOT NULL AND user_id IS NOT NULL
    """)

    twitter_users_table_insert = ("""
        SELECT distinct user_id, 
            username, 
            displayname, 
            description,
            followers_count,
            friends_count,
            statuses_count,
            favourites_count,
            listed_count,
            media_count
        FROM staging_tweets
        WHERE user_id IS NOT NULL
    """)

    tweet_stats_table_insert = ("""
        SELECT distinct tweet_id, reply_count, retweet_count, like_count, quote_count
        FROM staging_tweets
        WHERE tweet_id IS NOT NULL
    """)

    tweet_content_table_insert = ("""
        SELECT distinct tweet_id, content, language, url
        FROM staging_tweets
        WHERE tweet_id IS NOT NULL
    """)

    tweet_time_table_insert = ("""
        SELECT tweet_date, extract(hour from tweet_date), extract(day from tweet_date), extract(week from tweet_date), 
               extract(month from tweet_date), extract(year from tweet_date), extract(dayofweek from tweet_date)
        FROM tweets
    """)


    youtube_videos_table_insert = ("""
        SELECT distinct video_id,
               TIMESTAMP 'epoch' + published_at * interval '1 second' as published_at, 
               channel_id
        FROM staging_videos
        WHERE video_id IS NOT NULL
    """)


    youtube_video_content_table_insert = ("""
        SELECT distinct video_id,
            title,
            description,
            duration,
            dimension,
            definition,
            caption,
            licensed_content,
            projection
        FROM staging_videos
        WHERE video_id IS NOT NULL
    """)


    youtube_video_statistics_table_insert = ("""
        SELECT distinct video_id, view_count, like_count, favorite_count, comment_count
        FROM staging_videos
        WHERE video_id IS NOT NULL
    """)


    youtube_channel_table_insert = ("""
        SELECT distinct channel_id,
            channel_title,
            channel_description,
            channel_view_count,
            channel_subscriber_count,
            channel_hidden_subscriber_count,
            channel_video_count
        FROM staging_videos
        WHERE channel_id IS NOT NULL
    """)


    youtube_videos_time_table_insert = ("""
        SELECT published_at, extract(hour from published_at), extract(day from published_at), extract(week from published_at), 
               extract(month from published_at), extract(year from published_at), extract(dayofweek from published_at)
        FROM youtube_videos
    """)
