from django.urls import path, include

from .views import *

urlpatterns = [
  path("", home, name="home"),
  path("<int:alert>/", home, name="home"),
  path("contact/", contact, name="contact"),
  path("contactsent/", contactsent, name="contactsent"),
  path("released/", released, name="released"),
  path("about/", about, name="about"),
  path("current/", current, name="current"),
  path("r_group/<year_archived>/<r_num>/", current_r, name="current_r"),
  path("current/TurtleCreate/", TurtleCreate.as_view(extra_context = {'home_act': '', 'contact_act': '', 'released_act': '', 'about_act': '', 'current_act': 'active', 'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))}), name="TurtleCreate"),
  path("current/MeasurementCreate/", MeasurementCreate.as_view(extra_context = {'home_act': '', 'contact_act': '', 'released_act': '', 'about_act': '', 'current_act': 'active', 'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))}), name="MeasurementCreate"),
  path("accounts/", include("django.contrib.auth.urls")),
  path("logout/", logout_request, name="logout"),
  path("measurements.csv/", send_file, name='measurements.csv'),
  path("search/", search, name="search"),
  path('signup/', SignUp, name='signup'),
  path('confirm/<username>/', Confirm, name='confirm'),
  path('settings/<confirmation>/', settings, name='settings'),
  path('login/', userlogin, name='login'),
  path('forgot/', forgot, name='forgot'),
  path('history/measurement/<int:id>/', MeasurementHistory, name='MeasurementHistory'),
  path('history/turtle/<int:id>/', TurtleHistory, name='TurtleHistory'),
  path("current/MassTurtleCreate/", MassTurtleCreate, name='massturtlecreateform'),
]
