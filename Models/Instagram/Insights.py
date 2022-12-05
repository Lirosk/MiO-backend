from datetime import datetime
from typing import TypeVar, List, Optional
from enum import Enum
from Metrics import Metrics

TInsight = TypeVar('TInsight', bound='Insight')
TPeriod = TypeVar('TPeriod', bound='Periods')
TMetric = TypeVar('TMetric', bound='Metrics')
TInsightValue = TypeVar('TInsightValue', bound='InsightValue')

class Insight:
    '''
    Metric of IG users and their IG Media.
    '''
    name: TMetric
    period: TPeriod
    values: List[TInsightValue]
    title: str
    description: str
    id: str


class InsightValue:
    value: str | int
    end_time: Optional[datetime]


class Periods(Enum):
    DAY = 'day'
    DAYS_28 = 'days_28'
    MONTH = 'month'
    YEAR = 'year'
    LIFETIME = 'lifetime'
