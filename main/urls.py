from django.urls import path
from . import views

urlpatterns = [
    path("kanban/", views.KanbanAPIView.as_view(), name="kanban"),
    path("kanban/categories/", views.KanbanCategoriesAPIView.as_view(), name="kanban"),
    path("calendar/", views.CalendarAPIView.as_view(), name="calendar"),

    path("", views.SocialNetworkStatisticsAPIView.as_view()),
    path("<str:social_network>/", views.SocialNetworkStatisticsAPIView.as_view()),
    path("<str:social_network>/cancel/", views.CancelSocialNetworkAPIView.as_view()),
    path("<str:social_network>/authorize/", views.SocialNetworkAuthorizeAPIView.as_view()),
    path("<str:social_network>/authorized/", views.SocialNetworkAuthorizedAPIView.as_view()),
    path("<str:social_network>/<str:content_type>/", views.SocialNetworkStatisticsAPIView.as_view()),
    path("<str:social_network>/<str:content_type>/<str:metric>/", views.SocialNetworkStatisticsAPIView.as_view()),
]
