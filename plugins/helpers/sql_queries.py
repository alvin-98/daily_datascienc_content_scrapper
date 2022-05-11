class SqlQueries:
    tweets_table_insert = ("""
        SELECT distinct tweetId,
            tweetDate,
            userId,
            conversationId, 
            retweetedTweet, 
            quotedTweet, 
            inReplyToTweetId, 
            mentionedUsers, 
            hashtags, 
            place
        FROM (SELECT TIMESTAMP 'epoch' + tweetDate/1000 * interval '1 second' AS tweetDate, *
        FROM staging_tweets
        WHERE tweetId IS NOT NULL AND userId IS NOT NULL)
    """)

    twitter_users_table_insert = ("""
        SELECT distinct userId, 
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
            linkUrl
        FROM (SELECT TIMESTAMP 'epoch' + profileCreated/1000 * interval '1 second' AS profileCreated, * 
        FROM staging_tweets
        WHERE userId IS NOT NULL)
    """)

    tweet_stats_table_insert = ("""
        SELECT distinct tweetId, replyCount, retweetCount, likeCount, quoteCount
        FROM staging_tweets
        WHERE tweetId IS NOT NULL
    """)

    tweet_content_table_insert = ("""
        SELECT distinct tweetId, content, language, outlinks, media, hashtags, url
        FROM staging_tweets
        WHERE tweetId IS NOT NULL
    """)

    tweet_time_table_insert = ("""
        SELECT tweetDate, extract(hour from tweetDate), extract(day from tweetDate), extract(week from tweetDate), 
               extract(month from tweetDate), extract(year from tweetDate), extract(dayofweek from tweetDate)
        FROM tweets
    """)


    youtube_videos_table_insert = ("""
        SELECT videoId, publishedAt, channelId
        FROM staging_videos
        WHERE videoId IS NOT NULL
    """)


    youtube_video_content_table_insert = ("""
        SELECT videoId,
            title,
            description,
            duration,
            dimension,
            definition,
            caption,
            licensedContent,
            contentRating,
            projection
        FROM staging_videos
        WHERE videoId IS NOT NULL
    """)


    youtube_video_statistics_table_insert = ("""
        SELECT videoId, viewCount, likeCount, favoriteCount, commentCount
        FROM staging_videos
        WHERE videoId IS NOT NULL
    """)


    youtube_channel_table_insert = ("""
        SELECT channelId,
            channelTitle,
            channelDescription,
            channelCreatedOn,
            channelTopicCategories,
            channelViewCount,
            channelSubscriberCount,
            channelHiddenSubscriberCount,
            channelVideoCount
    """)


    youtube_videos_time_table_insert = ("""
        SELECT publishedAt, extract(hour from publishedAt), extract(day from publishedAt), extract(week from publishedAt), 
               extract(month from publishedAt), extract(year from publishedAt), extract(dayofweek from publishedAt)
        FROM youtube_videos
    """)
