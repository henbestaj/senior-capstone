# *************************************************************************************
#   File Name: urls.py
#   Purpose:
#     * Keep track of the urls used in the entire Django project
#     * Include urls from the urls.py file in every app that is a part of the project
#     * Create handlers for four simple errors that can often occur on the site
# *************************************************************************************

# Import statements
from django.contrib import admin
from django.urls import path, include

# Error handlers
handler404 = 'turtles.views.custom_page_not_found_view'
handler500 = 'turtles.views.custom_error_view'
handler403 = 'turtles.views.custom_permission_denied_view'
handler400 = 'turtles.views.custom_bad_request_view'

# List of all urls, the views they associate with, and the name that will be used to call them (including importing urls from the turtles urls.py file)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("turtles.urls")),

]