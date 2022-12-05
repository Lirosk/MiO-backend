from typing import List, TypeVar

TBusinessMediaData = TypeVar('TBusinessMediaData', bound='BusinessMediaData')

class BusinessDiscovery:
    '''
    Basic metadata and metrics about other Instagram Business and Creator Accounts.
    '''

    id: int
    followers_count: int
    media_count: int
    data: TBusinessMediaData


class BusinessMediaData:
    id: int
    data: List[dict[str, str | int]]
