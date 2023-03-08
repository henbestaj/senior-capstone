from django.shortcuts import render
from .models import Turtle, Measurement

# Create your views here.
def home(request):
  return render(request, 'turtles/home.html')

def contact(request):
  return render(request, 'turtles/contact.html')

def released(request):
  return render(request, 'turtles/released.html')

def about(request):
  return render(request, 'turtles/about.html')

def current(request):
  return render(request, 'turtles/current.html')

def signin(request):
  return render(request, 'turtles/signin.html')