from django.shortcuts import render, redirect
from .models import Turtle, Measurement
from django.views.generic.edit import CreateView
from .forms import *
import yagmail
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

# Create your views here.
def custom_page_not_found_view(request, exception):
    return render(request, "turtles/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "turtles/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "turtles/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "turtles/400.html", {})

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
  if request.method == 'POST':
    form = NewContactForm(request.POST)
    
    if form.is_valid():
      yag = yagmail.SMTP('terrapintrackercontact@gmail.com', oauth2_file = "./oauth2_creds.json")
      yag.send(to = ['henbestaj@gmail.com', 'lhiusnat@gmail.com', 'gangeloamato@gmail.com'], subject = str(form.cleaned_data["subject"]), contents = 'From:\n' + str(form.cleaned_data["email"]) + '\n\nMessage:\n' + str(form.cleaned_data["body"]))

      return redirect('/contactsent/')
  
  else:
    form = NewContactForm()

  context = {
    'home_act': '',
    'contact_act': 'active',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'form': form,
  }

  return render(request, 'turtles/contact.html', context)

def contactsent(request):
  context = {
    'home_act': '',
    'contact_act': 'active',
    'released_act': '',
    'about_act': '',
    'current_act': '',
  }
  return render(request, 'turtles/contactsent.html', context)

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
  plt.plot(list(Measurement.objects.all().values_list('carapace_width', flat = True)), list(Measurement.objects.all().values_list('mass', flat = True)))
  plt.savefig('./turtles/static/turtles/plot1.png')
  plt.close()
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.all(),
    'Measurement' : Measurement.objects.all(),
    'r_nums' : Turtle.objects.values('r_num').distinct(),
  }

  return render(request, 'turtles/current.html', context)

def current_turtle(request, r_num, hatchling_num):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.all(),
    'Measurement' : Measurement.objects.all(),
    'r' : int(r_num),
    'hatchling' : int(hatchling_num),
  }

  return render(request, 'turtles/current_turtle.html', context)

def current_r(request, r_num):
  carapace_width = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == int(r_num):
      carapace_width.append(measurement.carapace_width)
  mass = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == int(r_num):
      mass.append(measurement.mass)
  plt.plot(carapace_width, mass)
  file_path = './turtles/static/turtles/plot_r' + r_num + '.png'
  plt.savefig(file_path)
  plt.close()
  
  path = 'turtles/plot_r' + r_num + '.png'

  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.all(),
    'Measurement' : Measurement.objects.all(),
    'r' : int(r_num),
    'path' : path,
  }

  return render(request, 'turtles/current_r.html', context)

def login(request):
  return render(request, 'registration/login.html')

class TurtleCreate(LoginRequiredMixin, CreateView):
  model = Turtle
  form_class = NewTurtleCreateForm
  template_name = 'turtles/newturtlecreateform.html'
  success_url = '/current/'

class MeasurementCreate(LoginRequiredMixin, CreateView):
  model = Measurement
  form_class = NewMeasurementCreateForm
  template_name = 'turtles/newmeasurementcreateform.html'
  success_url = '/current/'

def logout_request(request):
  logout(request)
  return redirect("home")