from django.urls import path, re_path
from pipe import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events/by_name/<str:event_name>", views.get_event_by_name, name="by_name"),
    path("events/by_cost/<str:cost>", views.get_events_by_cost, name="by_cost"),
    path("events/by_sd/<str:timezone>/<str:local>/<str:utc>", views.get_by_timezone)
]
