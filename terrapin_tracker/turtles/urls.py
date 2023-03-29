from django.urls import path

from .views import *

urlpatterns = [
  path("", home, name="home"),
  path("contact/", contact, name="contact"),
  path("contactsent/", contactsent, name="contactsent"),
  path("released/", released, name="released"),
  path("about/", about, name="about"),
  path("current/", current, name="current"),
  path("signin/", signin, name="signin"),
  path("current/TurtleCreate/", TurtleCreate.as_view(), name="TurtleCreate"),
  path("current/MeasurementCreate/", MeasurementCreate.as_view(), name="MeasurementCreate"),
]
