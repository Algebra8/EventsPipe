from django.urls import path
from pipe import views

urlpatterns = [
    path("", views.index, name="index"),

]
