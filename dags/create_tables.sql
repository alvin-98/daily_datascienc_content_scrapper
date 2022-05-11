CREATE TABLE public.staging_tweets (
	url text,
	tweetDate timestamp,
	firstname varchar(256),
	content text,
	tweetId text NOT NULL PRIMARY KEY,
	replyCount int4,
	retweetCount int4,
	likeCount int4,
	quoteCount int4,
	conversationId text,
	language varchar(10),
	outlinks text,
	media text,
	song varchar(256),
	retweetedTweet text,
	quotedTweet text,
	inReplyToTweetId text,
	mentionedUsers text,
	hashtags text,
	place text,
	userId text,
	username text,
	displayname text,
	description text,
	descriptionUrls text,
	profileCreated text,
	followersCount int4,
	friendsCount int4,
	statusesCount int4,
	favouritesCount int4,
	listedCount int4,
	mediaCount int4,
	location text,
	linkUrl text
);

CREATE TABLE public.staging_videos (
	videoId text NOT NULL PRIMARY KEY,
	publishedAt timestamp,
	channelId text,
	title text,
	channelTitle text,
	description text,
	duration varchar(10),
	dimension varchar(10),
	definition varchar(10),
	caption boolean,
	licensedContent boolean,
	contentRating text,
	projection varchar(20),
	viewCount int4,
	likeCount int4,
	favoriteCount int4,
	commentCount int4,
	channelDescription text,
	channelCreatedOn timestamp,
	channelTopicCategories text, 
	channelViewCount int4,
	channelSubscriberCount int4,
	channelHiddenSubscriberCount boolean,
	channelVideoCount int4
);


CREATE TABLE public.tweets (
	tweetId text NOT NULL PRIMARY KEY,
	tweetDate timestamp NOT NULL,
	userId text NOT NULL,
	conversationId text,
	retweetedTweet text,
	quotedTweet text,
	inReplyToTweetId text,
	mentionedUsers text,
	hashtags text,
	place text
);

CREATE TABLE public.twitter_users (
	userId text NOT NULL PRIMARY KEY,
	username text,
	displayname text,
	description text,
	profileCreated timestamp,
	followersCount int4,
	friendsCount int4,
	statusesCount int4,
	favouritesCount varchar(256),
	listedCount int4,
	mediaCount int4,
	location text,
	linkUrl text
);

CREATE TABLE public.tweet_stats (
	tweetId text NOT NULL PRIMARY KEY,
	replyCount int4,
	retweetCount int4,
	likeCount int4,
	quoteCount int4
);

CREATE TABLE public.tweet_content (
	tweetId text NOT NULL PRIMARY KEY,
	content text NOT NULL,
	language varchar(10),
	outlinks text,
	media text,
	hashtags text,
	url text
);


CREATE TABLE public.tweet_time (
	tweetDate timestamp NOT NULL PRIMARY KEY,
	"hour" int4,
	"day" int4,
	week int4,
	"month" varchar(256),
	"year" int4,
	weekday varchar(256)
);


CREATE TABLE public.youtube_videos (
	videoId text NOT NULL PRIMARY KEY,
	publishedAt timestamp NOT NULL,
	channelId text NOT NULL
);


CREATE TABLE public.youtube_video_content (
	videoId text NOT NULL PRIMARY KEY,
	title text NOT NULL,
	description text,
	duration varchar(10) NOT NULL,
	dimension varchar(10),
	definition varchar(10),
	caption boolean,
	licensedContent boolean,
	contentRating text,
	projection varchar(20)
)


CREATE TABLE public.youtube_video_statistics (
	videoId text NOT NULL PRIMARY KEY,
	viewCount int4,
	likeCount int4,
	favoriteCount int4,
	commentCount int4
)


CREATE TABLE public.youtube_channel (
	channelId text NOT NULL PRIMARY KEY,
	channelTitle text NOT NULL,
	channelDescription text,
	channelCreatedOn timestamp,
	channelTopicCategories text,
	channelViewCount int4,
	channelSubscriberCount int4,
	channelHiddenSubscriberCount boolean,
	channelVideoCount int4
)


CREATE TABLE public.youtube_videos_time (
	publishedAt timestamp NOT NULL PRIMARY KEY,
	"hour" int4,
	"day" int4,
	week int4,
	"month" varchar(256),
	"year" int4,
	weekday varchar(256)
);
