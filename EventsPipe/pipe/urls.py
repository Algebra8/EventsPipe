from django.urls import path, re_path
from pipe import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events/search/", views.get_event, name="get_event"),
    path("events/update/by_id/<int:eventid>/", views.update_event, name="update_event"),
    path("events/dun/", views.dun)

]


# path("events/search/by_name/<str:event_name>", views.get_event_by_name, name="by_name"),
# path("events/search/by_cost/<str:cost>", views.get_events_by_cost, name="by_cost"),
# path("events/search/by_sd/<str:utc_startdate>", views.get_by_startdate, name="by_sd"),
