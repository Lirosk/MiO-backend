from django.urls import path
from . import views

urlpatterns = [
    path("kanban/", views.KanbanAPIView.as_view(), name="kanban"),
]
