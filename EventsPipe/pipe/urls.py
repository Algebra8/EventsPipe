from django.urls import path
from pipe import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("events/name/<str:event_name>", views.get_event_by_name, name="get_event_by_name"),
    # path("events/id/<int:eventid>", views.get_event_by_id, name="get_event_by_id"),
    # path("events/cost/<str:cost>", views.get_events_by_cost, name="get_events_by_cost"),
    path("events/<str:event_name>", views.get_all, name="get_all_name"),
    path("events/<int:eventid>", views.get_all, name="get_all_id"),


]
