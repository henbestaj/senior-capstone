# ************************************************************************************
#   File Name: urls.py
#   Purpose:
#     * Keep track of the urls used in the turtles Django app
#     * Associate each url with a view found in the views.py file
#     * Create a name for each url so that it can be easily referenced in html links
# ************************************************************************************

# Import statements
from django.urls import path, include
from .views import *

# List of all urls, the views they associate with, and the name that will be used to call them
urlpatterns = [
  path("", home, name="home"),
  path("<int:alert>/", home, name="home"),
  path("contact/", contact, name="contact"),
  path("contactsent/", contactsent, name="contactsent"),
  path("released/", released, name="released"),
  path("about/", about, name="about"),
  path("current/", current, name="current"),
  path("r_group/<int:year_archived>/<int:r_num>/", current_r, name="current_r"),
  path("deleted_r_group/<int:year_archived>/<int:r_num>/<int:year_deleted>/", current_r_deleted, name="current_r_deleted"),
  path("current/TurtleCreate/", TurtleCreate.as_view(extra_context = {'home_act': '', 'contact_act': '', 'released_act': '', 'about_act': '', 'current_act': 'active', 'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))}), name="TurtleCreate"),
  path("current/MeasurementCreate/", MeasurementCreate.as_view(extra_context = {'home_act': '', 'contact_act': '', 'released_act': '', 'about_act': '', 'current_act': 'active', 'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))}), name="MeasurementCreate"),
  path("accounts/", include("django.contrib.auth.urls")),
  path("logout/", logout_request, name="logout"),
  path("current_measurements.csv/", send_current_file, name='current_measurements.csv'),
  path("archived_measurements.csv/", send_archived_file, name='archived_measurements.csv'),
  path("search/", search, name="search"),
  path('signup/', SignUp, name='signup'),
  path('confirm/<username>/', Confirm, name='confirm'),
  path('settings/<confirmation>/', settings, name='settings'),
  path('login/', userlogin, name='login'),
  path('forgot/', forgot, name='forgot'),
  path('history/measurement/<int:id>/<deleted>/', MeasurementHistory, name='MeasurementHistory'),
  path('history/measurement/<int:id>/', MeasurementHistory, name='MeasurementHistory'),
  path('history/turtle/<int:id>/', TurtleHistory, name='TurtleHistory'),
  path('history/turtle/delete/<int:id>/', TurtleDelete, name='TurtleDelete'),
  path('history/measurement/delete/<int:id>/', MeasurementDelete, name='MeasurementDelete'),
  path("current/MassTurtleCreate/", MassTurtleCreate, name='massturtlecreateform'),
  path('current/MassArchive/', MassArchive, name='massarchive'),
  path('deleted/', Deleted, name='deleted'),
  path('r_group/deleted/<int:year_archived>/<int:r_num>/', DeletedMeasurement, name='DeletedMeasurement'),
]