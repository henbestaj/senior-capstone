from django.urls import path, include

from .views import *

urlpatterns = [
  path("", home, name="home"),
  path("contact/", contact, name="contact"),
  path("contactsent/", contactsent, name="contactsent"),
  path("released/", released, name="released"),
  path("about/", about, name="about"),
  path("current/", current, name="current"),
  path("current/<r_num>", current_r, name="current_r"),
  path("current/<r_num>/<hatchling_num>", current_turtle, name="current_turtle"),
  path("current/TurtleCreate/", TurtleCreate.as_view(), name="TurtleCreate"),
  path("current/MeasurementCreate/", MeasurementCreate.as_view(), name="MeasurementCreate"),
  path("accounts/", include("django.contrib.auth.urls")),
  path("logout/", logout_request, name="logout"),
]
