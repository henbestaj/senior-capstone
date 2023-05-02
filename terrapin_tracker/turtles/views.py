from django.utils import timezone, dateformat
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
  r_num = 3
  year_archived = 2023
  Turtle.objects.filter(archived = True, year_archived = 0).update(year_archived = int(dateformat.format(timezone.now(), 'Y')))
  
  measurements = []
  for i in Measurement.objects.all():
    if i.turtle.archived == False:
      measurements.append(i)
  
  r_nums = []
  for x in Turtle.objects.values('r_num').distinct():
    include = False
    for y in Turtle.objects.filter(r_num = x['r_num']):
      if (y.archived == False):
        include = True
    if include:
      r_nums.append(x['r_num'])


  date = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      date.append(measurement.date)
  turtle = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and r_num<=9 and measurement.turtle.year_archived == year_archived:
      turtle.append(measurement.display_turtle[2:])
    elif measurement.turtle.r_num == r_num and r_num>9 and measurement.turtle.year_archived == year_archived:
      turtle.append(measurement.display_turtle[3:])
  
  carapace_length = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_length.append(measurement.carapace_length)
  
  carapace_width = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_width.append(measurement.carapace_width)
  
  plastron_length = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      plastron_length.append(measurement.plastron_length)
  
  carapace_height = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_height.append(measurement.carapace_height)
  
  mass = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      mass.append(measurement.mass)
  
  fig, ax = plt.subplots()
  sns_plot = sns.scatterplot(ax=ax, x=carapace_height, y=mass).set_title('test')
  ax.set_xlabel( "Carapace Length" , size = 12 )
  ax.set_ylabel( "Carapace Width" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'test.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()
  path9 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'test.png'

  context= {
    'home_act': 'active',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'Turtle': Turtle.objects.filter(archived = False),
    'Measurement' : measurements,
    'r_nums' : r_nums,
    'year_archived' : 0,
    'path9' : path9,
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
  Turtle.objects.filter(archived = True, year_archived = 0).update(year_archived = int(dateformat.format(timezone.now(), 'Y')))

  measurements = []
  for i in Measurement.objects.all():
    if i.turtle.archived == True:
      measurements.append(i)
  
  r_nums = set()
  for x in Turtle.objects.filter(archived = True):
    r_nums.add((x.r_num, x.year_archived))
  r_nums = list(r_nums)
  r_nums = sorted(r_nums, key = lambda x: x[0])
  
  years = []
  for i in Turtle.objects.filter(archived = True).values('year_archived').distinct():
    years.append(i['year_archived'])
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': 'active',
    'about_act': '',
    'current_act': '',
    'Turtle': Turtle.objects.filter(archived = True),
    'Measurement' : measurements,
    'r_nums' : r_nums,
    'years' : years,
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

  Turtle.objects.filter(archived = True, year_archived = 0).update(year_archived = int(dateformat.format(timezone.now(), 'Y')))

  measurements = []
  for i in Measurement.objects.all():
    if i.turtle.archived == False:
      measurements.append(i)
  
  r_nums = []
  for x in Turtle.objects.values('r_num').distinct():
    include = False
    for y in Turtle.objects.filter(r_num = x['r_num']):
      if (y.archived == False):
        include = True
    if include:
      r_nums.append(x['r_num'])

  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.filter(archived = False),
    'Measurement' : measurements,
    'r_nums' : r_nums,
    'year_archived' : 0,
  }

  return render(request, 'turtles/current.html', context)

def current_turtle(request, year_archived, r_num, hatchling_num):
  year_archived = int(year_archived)
  r_num = int(r_num)
  hatchling_num = int(hatchling_num)
  
  no_turtles = True
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      no_turtles = False
  
  current_act = ''
  released_act = ''
  if year_archived == 0:
    current_act = 'active'
  else:
    released_act = 'active'
  
  context = {
    'no_turtles' : no_turtles,
    'home_act': '',
    'contact_act': '',
    'released_act': released_act,
    'about_act': '',
    'current_act': current_act,
    'Measurement' : Measurement.objects.all(),
    'r' : r_num,
    'hatchling' : hatchling_num,
    'year_archived' : year_archived,
  }

  return render(request, 'turtles/current_turtle.html', context)

def current_r(request, year_archived, r_num):
  r_num = int(r_num)
  year_archived = int(year_archived)

  no_turtles = True
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      no_turtles = False
  
  current_act = ''
  released_act = ''
  if year_archived == 0:
    current_act = 'active'
  else:
    released_act = 'active'

  if no_turtles:
    context = {
      'no_turtles' : no_turtles,
      'home_act': '',
      'contact_act': '',
      'released_act': released_act,
      'about_act': '',
      'current_act': current_act,
      'Turtle': Turtle.objects.all(),
      'Measurement' : Measurement.objects.all(),
      'r' : r_num,
    }

    return render(request, 'turtles/current_r.html', context)

  date = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      date.append(measurement.date)
  
  turtle = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and r_num<=9 and measurement.turtle.year_archived == year_archived:
      turtle.append(measurement.display_turtle[2:])
    elif measurement.turtle.r_num == r_num and r_num>9 and measurement.turtle.year_archived == year_archived:
      turtle.append(measurement.display_turtle[3:])
  
  carapace_length = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_length.append(measurement.carapace_length)
  
  carapace_width = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_width.append(measurement.carapace_width)
  
  plastron_length = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      plastron_length.append(measurement.plastron_length)
  
  carapace_height = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_height.append(measurement.carapace_height)
  
  mass = []
  for measurement in Measurement.objects.all():
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      mass.append(measurement.mass)
  
  fig, ax = plt.subplots()
  sns_plot = sns.scatterplot(ax=ax, x=carapace_length, y=carapace_width, hue=date).set_title('Carapace Length vs Carapace Width')
  ax.set_xlabel( "Carapace Length" , size = 12 )
  ax.set_ylabel( "Carapace Width" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvswidthscatter.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.kdeplot(ax=ax, x=carapace_length, y=carapace_width, fill=True, cmap="crest").set_title('Carapace Length vs Carapace Width')
  ax.set_xlabel( "Carapace Length" , size = 12 )
  ax.set_ylabel( "Carapace Width" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvswidthkde.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.boxplot(ax=ax, x=date, y=carapace_length, palette='Blues').set_title('Carapace Length over Time')
  ax.set_xlabel( "Measurement Date" , size = 12 )
  ax.set_ylabel( "Carapace Length" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'datevslengthbar.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.scatterplot(ax=ax, x=plastron_length, y=carapace_height, hue=date).set_title('Plastron Length vs Carapace Height')
  ax.set_xlabel( "Plastron Length" , size = 12 )
  ax.set_ylabel( "Carapace Height" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvsheightscatter.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.kdeplot(ax=ax, x=plastron_length, y=carapace_height, fill=True, cmap='crest').set_title('Plastron Length vs Carapace Height')
  ax.set_xlabel( "Plastron Length" , size = 12 )
  ax.set_ylabel( "Carapace Height" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvsheightkde.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.boxplot(ax=ax, x=date, y=carapace_height, palette='Blues').set_title('Carapace Height over Time')
  ax.set_xlabel( "Measurement Date" , size = 12 )
  ax.set_ylabel( "Carapace Height" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'datevsheightbox.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.histplot(ax=ax, x=mass, bins='auto', palette='Oranges').set_title('Turtle Mass Distribution')
  ax.set_xlabel( "Mass" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'masshist.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.barplot(ax=ax, x=turtle, y=mass, palette='light:orange').set_title('Mass of Turtle by Hatchling Number')
  ax.set_xlabel( "Turtle Number" , size = 12 )
  ax.set_ylabel( "Mass" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'turtlevsheightbox.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  # fig, ax = plt.subplots()
  # sns_plot = sns.barplot(ax=ax, x=r_nums, y=mass, palette='light:orange').set_title('test')
  # ax.set_xlabel( "Turtle Number" , size = 12 )
  # ax.set_ylabel( "Mass" , size = 12 )
  # file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'test.png'
  # fig = sns_plot.get_figure()
  # fig.savefig(file_path)
  # plt.clf()
  
  path1 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvswidthscatter.png'
  path2 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvswidthkde.png'
  path3 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'datevslengthbar.png'
  path4 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvsheightscatter.png'
  path5 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvsheightkde.png'
  path6 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'datevsheightbox.png'
  path7 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'masshist.png'
  path8 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'turtlevsheightbox.png'
  path9 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'test.png'


  context = {
    'no_turtles' : no_turtles,
    'home_act': '',
    'contact_act': '',
    'released_act': released_act,
    'about_act': '',
    'current_act': current_act,
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
    'path8' : path8,
    'path9' : path9,
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