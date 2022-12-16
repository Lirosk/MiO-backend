from django.urls import path
from . import views

urlpatterns = [
    path("kanban/", views.KanbanAPIView.as_view(), name="kanban"),
    path("kanban/categories/", views.KanbanCategoriesAPIView.as_view(), name="kanban"),
    path("calendar/", views.CalendarAPIView.as_view(), name="calendar"),
]
