from django.urls import path, include

from .views import *

urlpatterns = [
  path("", home, name="home"),
  path("contact/", contact, name="contact"),
  path("contactsent/", contactsent, name="contactsent"),
  path("released/", released, name="released"),
  path("about/", about, name="about"),
  path("current/", current, name="current"),
  path("<year_archived>/<r_num>", current_r, name="current_r"),
  path("current/TurtleCreate/", TurtleCreate.as_view(extra_context = {'home_act': '', 'contact_act': '', 'released_act': '', 'about_act': '', 'current_act': 'active', }), name="TurtleCreate"),
  path("current/MeasurementCreate/", MeasurementCreate.as_view(extra_context = {'home_act': '', 'contact_act': '', 'released_act': '', 'about_act': '', 'current_act': 'active', }), name="MeasurementCreate"),
  path("accounts/", include("django.contrib.auth.urls")),
  path("logout/", logout_request, name="logout"),
  path("measurements.csv/", send_file, name='measurements.csv')
]
