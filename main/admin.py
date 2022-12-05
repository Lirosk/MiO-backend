from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CalendarEvent)
admin.site.register(KanbanCategories)
admin.site.register(KanbanEvent)
admin.site.register(SocialNetwork)
admin.site.register(ContentType)
admin.site.register(StatisticMetric)
admin.site.register(MetricValue)