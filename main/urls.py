from django.urls import path
from . import views

urlpatterns = [
    path("kanban/", views.KanbanAPIView.as_view(), name="kanban"),
    path("kanban/categories/", views.KanbanCategoriesAPIView.as_view(), name="kanban"),
    path("calendar/", views.CalendarAPIView.as_view(), name="calendar"),
    path("google/authorize/", views.GoogleAuthorizeAPIView.as_view(), name="google-authorize"),
    path("google/authorized/", views.GoogleAuthorizedAPIView.as_view(), name="google-authorized"),

    path("", views.SocialNetworkStatisticsAPIView.as_view()),
    path("<str:social_network>/", views.SocialNetworkStatisticsAPIView.as_view()),
    path("<str:social_network>/<str:content_type>/", views.SocialNetworkStatisticsAPIView.as_view()),
    path("<str:social_network>/<str:content_type>/<str:metric>/", views.SocialNetworkStatisticsAPIView.as_view()),
]
