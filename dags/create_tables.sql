DROP TABLE IF EXISTS public.staging_tweets;
DROP TABLE IF EXISTS public.staging_videos;


CREATE TABLE IF NOT EXISTS public.staging_tweets (
    url varchar(max),
    tweet_date int8,
    content varchar(max),
    tweet_id text PRIMARY KEY,
    reply_count int8,
    retweet_count int8,
    like_count int8,
    quote_count int8,
    conversation_id text,
    language varchar(10),
    retweeted_tweet_id varchar(max),
    quoted_tweet_id varchar(max),
    inreply_to_tweet_id text,
    user_id text,
    username text,
    displayname text,
    description varchar(max),
    followers_count int8,
    friends_count int8,
    statuses_count int8,
    favourites_count int8,
    listed_count int8,
    media_count int8
);

CREATE TABLE IF NOT EXISTS public.staging_videos (
    video_id text PRIMARY KEY,
    published_at int8,
    channel_id text,
    title text,
    channel_title text,
    description varchar(max),
    duration varchar(20),
    dimension varchar(10),
    definition varchar(10),
    caption varchar(10),
    licensed_content varchar(10),
    projection varchar(20),
    view_count int8,
    like_count int8,
    favorite_count int8,
    comment_count int8,
    channel_description varchar(max),
    channel_view_count int8,
    channel_subscriber_count int8,
    channel_hidden_subscriber_count varchar(10),
    channel_video_count int8
);


CREATE TABLE IF NOT EXISTS public.tweets (
    tweet_id text NOT NULL PRIMARY KEY,
    tweet_date timestamp NOT NULL,
    user_id text NOT NULL,
    conversation_id text,
    retweeted_tweet_id varchar(max),
    quoted_tweet_id varchar(max),
    inreply_to_tweet_id text
);

CREATE TABLE IF NOT EXISTS public.twitter_users (
    user_id text NOT NULL PRIMARY KEY,
    username text,
    displayname text,
    description varchar(max),
    followers_count int8,
    friends_count int8,
    statuses_count int8,
    favourites_count int8,
    listed_count int8,
    media_count int8
);

CREATE TABLE IF NOT EXISTS public.tweet_stats (
    tweet_id text NOT NULL PRIMARY KEY,
    reply_count int8,
    retweet_count int8,
    like_count int8,
    quote_count int8
);

CREATE TABLE IF NOT EXISTS public.tweet_content (
    tweet_id text NOT NULL PRIMARY KEY,
    content varchar(max) NOT NULL,
    language varchar(10),
    url varchar(max)
);


CREATE TABLE IF NOT EXISTS public.tweet_time (
    tweet_date timestamp NOT NULL PRIMARY KEY,
    "hour" int8,
    "day" int8,
    week int8,
    "month" varchar(256),
    "year" int8,
    weekday varchar(256)
);


CREATE TABLE IF NOT EXISTS public.youtube_videos (
    video_id text NOT NULL PRIMARY KEY,
    published_at timestamp NOT NULL,
    channel_id text NOT NULL
);


CREATE TABLE IF NOT EXISTS public.youtube_video_content (
    video_id text NOT NULL PRIMARY KEY,
    title text NOT NULL,
    description varchar(max),
    duration varchar(20) NOT NULL,
    dimension varchar(10),
    definition varchar(10),
    caption varchar(10),
    licensed_content varchar(10),
    projection varchar(20)
);


CREATE TABLE IF NOT EXISTS public.youtube_video_statistics (
    video_id text NOT NULL PRIMARY KEY,
    view_count int8,
    like_count int8,
    favorite_count int8,
    comment_count int8
);


CREATE TABLE IF NOT EXISTS public.youtube_channel (
    channel_id text NOT NULL PRIMARY KEY,
    channel_title text NOT NULL,
    channel_description varchar(max),
    channel_view_count int8,
    channel_subscriber_count int8,
    channel_hidden_subscriber_count varchar(10),
    channel_video_count int8
);


CREATE TABLE IF NOT EXISTS public.youtube_videos_time (
    published_at timestamp NOT NULL PRIMARY KEY,
    "hour" int8,
    "day" int8,
    week int8,
    "month" varchar(256),
    "year" int8,
    weekday varchar(256)
);


