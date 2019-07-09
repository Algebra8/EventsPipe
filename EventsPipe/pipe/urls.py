from django.urls import path, re_path
from pipe import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events/search/", views.get_event, name="get_event"),
    path("events/update/<int:eventid>", views.update_event, name="update_event"),
]
