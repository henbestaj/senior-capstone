from django.shortcuts import render
from .models import Turtle, Measurement

# Create your views here.
def home(request):
  return render(request, 'turtles/home.html')