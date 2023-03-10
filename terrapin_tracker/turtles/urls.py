from django.urls import path

from .views import *

urlpatterns = [
  path("", home, name="home"),
  path("contact/", contact, name="contact"),
  path("released/", released, name="released"),
  path("about/", about, name="about"),
  path("current/", current, name="current"),
  path("signin/", signin, name="signin"),
]
