from django.shortcuts import render
from .models import Turtle, Measurement

# Create your views here.
def home(request):
  context = {
    'home_act': 'active',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
  }
  return render(request, 'turtles/home.html', context)

def contact(request):
  context = {
    'home_act': '',
    'contact_act': 'active',
    'released_act': '',
    'about_act': '',
    'current_act': '',
  }
  return render(request, 'turtles/contact.html', context)

def released(request):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': 'active',
    'about_act': '',
    'current_act': '',
  }
  return render(request, 'turtles/released.html', context)

def about(request):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': 'active',
    'current_act': '',
  }
  return render(request, 'turtles/about.html', context)

def current(request):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.all(),
    'Measurment': Measurement.objects.all(),
  }
  return render(request, 'turtles/current.html', context)

def signin(request):
  return render(request, 'turtles/signin.html')