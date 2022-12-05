from typing import TypeVar, List
x
TStatistics = TypeVar('TStatistics', bound='Statistics')


class Channel:
    id: int
    '''
    The ID that YouTube uses to uniquely identify the channel.
    '''

    statistics: TStatistics
    '''
    Encapsulated statistics for the channel.
    '''


class Statistics:
    view_count: int
    '''
    The number of times the channel has been viewed.
    '''

    subscriber_count: int
    '''
    The number of subscribers that the channel has. This value is rounded down to three significant figures.
    '''

    video_count: int
    '''
    The number of public videos uploaded to the channel. Note that the value reflects the count of the channel's public videos only, even to owners.
    '''
