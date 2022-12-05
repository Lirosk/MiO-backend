from enum import Enum


class AccountMetrics(Enum):
    IMPRESSIONS = 'impressions'
    '''
    Total number of times the IG User's IG Media have been viewed. Includes ad activity generated through the API, Facebook ads interfaces, and the Promote feature. Does not include profile views.
    '''

    REACH = 'reach'
    '''
    Total number of unique users who have viewed at least one of the IG User's IG Media. Repeat views and views across different IG Media owned by the IG User by the same user are only counted as a single view. Includes ad activity generated through the API, Facebook ads interfaces, and the Promote feature.
    '''

    PROFILE_VIEWS = 'profile_views'
    '''
    Total number of users who have viewed the IG User's profile within the specified period.
    '''

    FOLLOWER_COUNT = 'follower_count'
    '''
    Total number of new followers each day within the specified range. Returns a maximum of 30 days worth of data. Not available on IG Users with fewer than 100 followers.
    '''

    ONLINE_FOLLOWERS = 'online_followers'
    '''
    Total number of the IG User's followers who were online during the specified range. Not available on IG Users with fewer than 100 followers.
    '''

    AUDIENCE_CITY = 'audience_city'
    '''
    Cities of followers for whom we have demographic data.
    '''

    AUDIENCE_COUNTRY = 'audience_country'
    '''
    Countries of followers for whom we have demographic data.
    '''

    AUDIENCE_GENDER_AGE = 'audience_gender_age'
    '''
    The gender and age distribution of followers for whom we have demographic data. Possible values: M (male), F (female), U (unknown).
    '''

    AUDIENCE_LOCALE = 'audience_locale'
    '''
    Locales by country codes of followers for whom we have demographic data.
    '''

    EMAIL_CONTACTS = 'email_contacts'
    '''	
    Total number of taps on the email link in the IG User's profile.
    '''

    GET_DIRECTIONS_CLICKS = 'get_directions_clicks'
    '''
    Total number of taps on the directions link in the IG User's profile.
    '''

    TEXT_MESSAGE_CLICKS = 'text_message_clicks'
    '''
    Total number of taps on the text message link in the IG User's profile.
    '''

    WEBSITE_CLICKS = 'website_clicks'
    '''
    Total number of taps on the website link in the IG User's profile.
    '''


class MediaMetrics(Enum):
    IMPRESSIONS = 'impressions'
    '''
    Total number of times the IG User's IG Media have been viewed. Includes ad activity generated through the API, Facebook ads interfaces, and the Promote feature. Does not include profile views.
    '''

    REACH = 'reach'
    '''
    Total number of unique users who have viewed at least one of the IG User's IG Media. Repeat views and views across different IG Media owned by the IG User by the same user are only counted as a single view. Includes ad activity generated through the API, Facebook ads interfaces, and the Promote feature.
    '''

    ENGAGEMENT = 'engagement'
    '''
    Sum of likes_count, comment_count, and saved counts on the IG Media.
    '''

    SAVED = 'saved'
    '''	
    Total number of unique Instagram accounts that have saved the IG Media object.
    '''

    VIDEO_VIEWS = 'video_views'
    '''
    Total number of times the video IG Media has been seen. For album IG Media, the number of times all videos within the album have been seen.
    '''


class ReelsMetrics(Enum):
    COMMENTS = 'comments'
    '''
    Number of comments on the reel. Metric in development.
    '''

    LIKES = 'likes'
    '''
    Number of likes on the reel. Metric in development.
    '''

    PLAYS = 'plays'
    '''
    Number of times the reels starts to play after an impression is already counted. This is defined as video sessions with 1 ms or more of playback and excludes replays. Metric in development.
    '''

    REACH = 'reach'
    '''
    Number of unique accounts that have seen the reel at least once. Reach is different from impressions, which can include multiple views of a reel by the same account. Metric is estimated and in development.
    '''

    SAVED = 'saved'
    '''
    Number of saves of the reel. Metric in development.
    '''

    SHARES = 'shares'
    '''	
    Number of shares of the reel. Metric in development.
    '''

    TOTAL_INTERACTIONS = 'total_interactions'
    '''
    Number of likes, saves, comments, and shares on the reel, minus the number of unlikes, unsaves, and deleted comments. Metric in development.
    '''


class StoryMetrics(Enum):
    EXITS = 'exits'
    '''
    Total number of times someone exited the story IG Media object.
    '''

    IMPRESSIONS = 'impressions'
    '''
    Total number of times the story IG Media object has been seen.
    '''

    REACH = 'reach'
    '''
    Total number of unique Instagram accounts that have seen the story IG Media object.
    '''

    REPLIES = 'replies'
    '''	
    Total number of replies (IG Comments) on the story IG Media object. Value does not include replies made by users in some regions. These regions include: Europe starting December 1, 2020 and Japan starting April 14, 2021. If the Story was created by a user in one of these regions, returns a value of 0.
    '''

    TAPS_FORWARD = 'taps_forward'
    '''
    Total number of taps to see this story IG Media object's next photo or video.
    '''

    TAPS_BACK = 'taps_back'
    '''
    Total number of taps to see this story IG Media object's previous photo or video.
    '''


class AlbumMetrics(Enum):
    CAROUSEL_ALBUM_ENGAGEMENT = 'carousel_album_engagement'
    '''
    Total number of likes and IG Comments on the album IG Media object.
    '''

    CAROUSEL_ALBUM_IMPRESSIONS = 'carousel_album_impressions'
    '''
    Total number of times the album IG Media object has been seen.
    '''

    CAROUSEL_ALBUM_REACH = 'carousel_album_reach'
    '''
    Total number of unique Instagram accounts that have seen the album IG Media object.
    '''

    CAROUSEL_ALBUM_SAVED = 'carousel_album_saved'
    '''
    Total number of unique Instagram accounts that have saved the album IG Media object.
    '''

    CAROUSEL_ALBUM_VIDEO_VIEWS = 'carousel_album_video_views'
    '''
    Total number of unique Instagram accounts that have viewed video IG Media within the album.
    '''


class PhotoAndVideoMetrics(Enum):
    ENGAGEMENT = 'engagement'
    '''
    Sum of likes_count, comment_count, and saved counts on the IG Media.
    '''

    IMPRESSIONS = 'impressions'
    '''
    Total number of times the IG Media object has been seen.
    '''

    REACH = 'reach'
    '''	
    Total number of unique Instagram accounts that have seen the IG Media object.
    '''

    SAVED = 'saved'
    '''
    Total number of unique Instagram accounts that have saved the IG Media object.
    '''

    VIDEO_VIEWS = 'video_views'
    '''
    Total number of times the video IG Media has been seen. For album IG Media, the number of times all videos within the album have been seen.
    '''


class Metrics(
    AccountMetrics,
    MediaMetrics,
    ReelsMetrics,
    StoryMetrics,
    AlbumMetrics,
    PhotoAndVideoMetrics
):
    ...
