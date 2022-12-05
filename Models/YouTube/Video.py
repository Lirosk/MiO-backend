from datetime import datetime
from typing import TypeVar

TStatistics = TypeVar('TStatistics', bound='Statistics')


class Video:
    id: int
    '''
    The ID that YouTube uses to uniquely identify the channel.
    '''

    create_time: datetime
    '''
    UTC Unix epoch (in seconds) of when the TikTok video was posted.
    '''

    statistics: TStatistics


class Statistics:
    view_count: int
    '''
    The number of times the video has been viewed.
    '''

    like_count: int
    '''
    The number of users who have indicated that they liked the video.
    '''

    dislike_count: int
    '''
    The number of users who have indicated that they disliked the video.
    '''

    comment_count: int
    '''
    The number of comments for the video.
    '''
