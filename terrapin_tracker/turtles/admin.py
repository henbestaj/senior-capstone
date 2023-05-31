# *******************************************************************************
#   File Name: admin.py
#   Purpose:
#     * Provide additional uses for the Django automatically created admin page
# *******************************************************************************

# Import statements
from django.contrib import admin
from .models import Turtle, Measurement

# Register the two models to the admin site so administrators can view and edit them directly
admin.site.register(Turtle)
admin.site.register(Measurement)