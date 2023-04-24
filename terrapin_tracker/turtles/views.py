from datetime import datetime
from django.shortcuts import render, redirect
from .models import Turtle, Measurement
from django.views.generic.edit import CreateView
from .forms import *
import yagmail
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import seaborn as sns
sns.set()
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
  r_num = int(r_num)
  hatchling_num = int(hatchling_num)
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.all(),
    'Measurement' : Measurement.objects.all(),
    'r' : r_num,
    'hatchling' : hatchling_num,
  }

  return render(request, 'turtles/current_turtle.html', context)

def current_r(request, r_num):
  if r_num != 'script.js':
    r_num = int(r_num)
    date = []
    for measurement in Measurement.objects.all():
      if measurement.turtle.r_num == r_num:
        date.append(measurement.date)
    turtle = []
    for measurement in Measurement.objects.all():
      if measurement.turtle.r_num == r_num:
        turtle.append(measurement.display_turtle)
    carapace_length = []
    for measurement in Measurement.objects.all():
      if measurement.turtle.r_num == r_num:
        carapace_length.append(measurement.carapace_length)
    carapace_width = []
    for measurement in Measurement.objects.all():
      if measurement.turtle.r_num == r_num:
        carapace_width.append(measurement.carapace_width)
    plastron_length = []
    for measurement in Measurement.objects.all():
      if measurement.turtle.r_num == r_num:
        plastron_length.append(measurement.plastron_length)
    carapace_height = []
    for measurement in Measurement.objects.all():
      if measurement.turtle.r_num == r_num:
        carapace_height.append(measurement.carapace_height)
    mass = []
    for measurement in Measurement.objects.all():
      if measurement.turtle.r_num == r_num:
        mass.append(measurement.mass)
    

    sns_plot = sns.scatterplot(x=carapace_length, y=carapace_width, hue=date)
    file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'lengthvswidthscatter.png'
    fig = sns_plot.get_figure()
    fig.savefig(file_path)
    plt.clf()

    sns_plot = sns.scatterplot(x=plastron_length, y=carapace_height, hue=date)
    file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'lengthvsheightscatter.png'
    fig = sns_plot.get_figure()
    fig.savefig(file_path)
    plt.clf()
  
    sns_plot = sns.boxplot(x=date, y=carapace_height)
    file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'datevsheightbox.png'
    fig = sns_plot.get_figure()
    fig.savefig(file_path)
    plt.clf()

    sns_plot = sns.barplot(x=date, y=carapace_length)
    file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'datevslengthbar.png'
    fig = sns_plot.get_figure()
    fig.savefig(file_path)
    plt.clf()

    sns_plot = sns.kdeplot(x=carapace_length, y=carapace_width)
    file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'lengthvswidthkde.png'
    fig = sns_plot.get_figure()
    fig.savefig(file_path)
    plt.clf()

    sns_plot = sns.histplot(x=mass, bins='auto')
    file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'masshist.png'
    fig = sns_plot.get_figure()
    fig.savefig(file_path)
    plt.clf()

    sns_plot = sns.boxplot(x=turtle, y=mass)
    file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'turtlevsheightbox.png'
    fig = sns_plot.get_figure()
    fig.savefig(file_path)
    plt.clf()
  
  path1 = 'turtles/plot_r' + str(r_num) + 'lengthvswidthscatter.png'
  path2 = 'turtles/plot_r' + str(r_num) + 'lengthvsheightscatter.png'
  path3 = 'turtles/plot_r' + str(r_num) + 'datevsheightbox.png'
  path4 = 'turtles/plot_r' + str(r_num) + 'datevslengthbar.png'
  path5 = 'turtles/plot_r' + str(r_num) + 'lengthvswidthkde.png'
  path6 = 'turtles/plot_r' + str(r_num) + 'masshist.png'
  path7 = 'turtles/plot_r' + str(r_num) + 'turtlevsheightbox.png'





  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.all(),
    'Measurement' : Measurement.objects.all(),
    'r' : r_num,
    'path1' : path1,
    'path2' : path2,
    'path3' : path3,
    'path4' : path4,
    'path5' : path5,
    'path6' : path6,
    'path7' : path7,
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