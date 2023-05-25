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
import csv
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import string

# Create your views here.
@login_required
def Deleted(request):
  measurements = []
  for i in Measurement.objects.exclude(valid_to = None):
    if not Measurement.objects.filter(previous_measurment = i).exists():
      measurements.append(i)
  
  r_nums = set()
  for x in Turtle.objects.exclude(valid_to = None):
    if not Turtle.objects.filter(previous_turtle = x).exists():
      r_nums.add((x.r_num, x.valid_to.year, x.year_archived))
  r_nums = list(r_nums)
  r_nums = sorted(r_nums, key = lambda x: x[0])
  
  years = set()
  for i in r_nums:
    years.add(i[1])
  years = list(years)
  years = sorted(years)

  turtles = []
  for i in Turtle.objects.exclude(valid_to = None):
    if not Turtle.objects.filter(previous_turtle = i).exists():
      turtles.append(i)

  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': 'active',
    'about_act': '',
    'current_act': '',
    'Turtle': turtles,
    'Measurement' : measurements,
    'r_nums' : r_nums,
    'years' : years,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/deleted.html', context)

@login_required
def MassArchive(request):
  if request.method == 'POST':
    form = MassArchiveForm(request.POST)

    if form.is_valid():
      for i in form.cleaned_data['individual_turtles']:
        new = Turtle(r_num = Turtle.objects.get(id = i).r_num, hatchling_num = Turtle.objects.get(id = i).hatchling_num, archived = True, year_archived = int(dateformat.format(timezone.now(), 'Y')), previous_turtle = Turtle.objects.get(id = i), editor = request.user.first_name + ' ' + request.user.last_name + ' (' + request.user.email + ')')
        new.save()
        Measurement.objects.filter(turtle = Turtle.objects.get(id = i)).update(turtle = new)
        Turtle.objects.filter(valid_to = None, archived = False, id = i).update(valid_to = timezone.now())

      for i in form.cleaned_data['r_num_field']:
        for x in Turtle.objects.filter(valid_to = None, archived = False, r_num = i):
          new = Turtle(r_num = i, hatchling_num = x.hatchling_num, archived = True, year_archived = int(dateformat.format(timezone.now(), 'Y')), previous_turtle = x, editor = request.user.first_name + ' ' + request.user.last_name + ' (' + request.user.email + ')')
          new.save()
          Measurement.objects.filter(turtle = x).update(turtle = new)
        Turtle.objects.filter(valid_to = None, archived = False, r_num = i).update(valid_to = timezone.now())
      
      return redirect('released')
  
  else:
    form = MassArchiveForm()
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7)),
    'form': form,
  }

  return render(request, 'turtles/MassArchive.html', context)

@login_required
def MassTurtleCreate(request):
  if request.method == 'POST':
    form = MassTurtleCreateForm(request.POST)
    if form.is_valid():
      for x in range(form.cleaned_data['r_num1'], form.cleaned_data['r_num2'] + 1):
        for y in range(form.cleaned_data['hatchling_num1'], form.cleaned_data['hatchling_num2'] + 1):
          new = Turtle(r_num = x, hatchling_num = y, editor = form.cleaned_data['editor'])
          new.save()
      return redirect('current')
  else:
    form = MassTurtleCreateForm(initial={'editor': request.user.first_name + ' ' + request.user.last_name + ' (' + request.user.email + ')'})
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'form': form,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/massturtlecreateform.html', context)

@login_required
def MeasurementHistory(request, id):
  current_act = ''
  released_act = ''
  if Measurement.objects.get(valid_to = None, id = id).turtle.year_archived == 0:
    current_act = 'active'
  else:
    released_act = 'active'
  
  original = id

  history = [Measurement.objects.get(valid_to = None, id = id)]
  while Measurement.objects.get(id = id).previous_measurment != None:
    id = Measurement.objects.get(id = id).previous_measurment.id
    history.append(Measurement.objects.get(id = id))

  id = original

  if request.method == 'POST':
    form = EditMeasurementCreateForm(request.POST)
    
    if form.is_valid():
      Measurement.objects.filter(valid_to = None, id = id).update(valid_to = timezone.now())
      new = Measurement(date = form.cleaned_data['date'], carapace_length = form.cleaned_data['carapace_length'], carapace_width = form.cleaned_data['carapace_width'], plastron_length = form.cleaned_data['plastron_length'], carapace_height = form.cleaned_data['carapace_height'], mass = form.cleaned_data['mass'], turtle = form.cleaned_data['turtle'], previous_measurment = Measurement.objects.get(id = id), editor = request.user.first_name + ' ' + request.user.last_name + ' (' + request.user.email + ')')
      new.save()
      return redirect('current_r', form.cleaned_data['turtle'].year_archived, form.cleaned_data['turtle'].r_num)
  
  else:
    form = EditMeasurementCreateForm(initial={'id': id, 'date': Measurement.objects.get(id = id).date, 'carapace_length': Measurement.objects.get(id = id).carapace_length, 'carapace_width': Measurement.objects.get(id = id).carapace_width, 'plastron_length': Measurement.objects.get(id = id).plastron_length, 'carapace_height': Measurement.objects.get(id = id).carapace_height, 'mass': Measurement.objects.get(id = id).mass, 'turtle': Measurement.objects.get(id = id).turtle})

  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': released_act,
    'about_act': '',
    'current_act': current_act,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7)),
    'history': history,
    'form': form,
    'id' : id,
  }

  return render(request, 'turtles/MeasurementHistory.html', context)

@login_required
def TurtleHistory(request, id):
  current_act = ''
  released_act = ''
  if Turtle.objects.get(id = id).year_archived == 0:
    current_act = 'active'
  else:
    released_act = 'active'
  
  original = id

  history = [Turtle.objects.get(id = id)]
  while Turtle.objects.get(id = id).previous_turtle != None:
    id = Turtle.objects.get(id = id).previous_turtle.id
    history.append(Turtle.objects.get(id = id))
  
  id = original

  if request.method == 'POST':
    if Turtle.objects.get(id = id).archived:
      form = EditTurtleCreateFormArchived(request.POST)
    else:
      form = EditTurtleCreateForm(request.POST)
    
    _mutable = form.data._mutable
    form.data._mutable = True

    if 'archived' not in form.data:
      form.data['archived'] = False
    else:
      form.data['archived'] = True

    if form.data['archived'] and not Turtle.objects.get(id = id).archived:
      form.data['year_archived'] = int(dateformat.format(timezone.now(), 'Y'))
    elif not form.data['archived'] and Turtle.objects.get(id = id).archived:
      form.data['year_archived'] = 0
    else:
      form.data['year_archived'] = form.data['year_archived']
    
    form.data._mutable = _mutable

    if form.is_valid():
      Turtle.objects.filter(valid_to = None, id = id).update(valid_to = timezone.now())
      new = Turtle(r_num = form.cleaned_data['r_num'], hatchling_num = form.cleaned_data['hatchling_num'], archived = form.cleaned_data['archived'], year_archived = form.cleaned_data['year_archived'], previous_turtle = Turtle.objects.get(id = id), editor = request.user.first_name + ' ' + request.user.last_name + ' (' + request.user.email + ')')
      new.save()
      Measurement.objects.filter(turtle = Turtle.objects.get(id = id)).update(turtle = new)
      if form.cleaned_data['archived']:
        return redirect('released')
      else:
        return redirect('current')
  
  else:
    if Turtle.objects.get(id = id).archived:
      form = EditTurtleCreateFormArchived(initial={'id': id, 'r_num': Turtle.objects.get(id = id).r_num, 'hatchling_num': Turtle.objects.get(id = id).hatchling_num, 'year_archived': Turtle.objects.get(id = id).year_archived})
    else:
      form = EditTurtleCreateForm(initial={'id': id, 'r_num': Turtle.objects.get(id = id).r_num, 'hatchling_num': Turtle.objects.get(id = id).hatchling_num, 'year_archived': Turtle.objects.get(id = id).year_archived})
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': released_act,
    'about_act': '',
    'current_act': current_act,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7)),
    'history': history,
    'form': form,
    'id' : id,
  }

  return render(request, 'turtles/TurtleHistory.html', context)

@login_required
def TurtleDelete(request, id):
  current_act = ''
  released_act = ''
  if Turtle.objects.get(id = id).year_archived == 0:
    current_act = 'active'
  else:
    released_act = 'active'
  
  if request.method == 'POST':
    form = TurtleDeleteForm(request.POST)

    if form.is_valid():
      Turtle.objects.filter(valid_to = None, id = id).update(valid_to = timezone.now())
      Measurement.objects.filter(turtle = Turtle.objects.get(id = id)).update(valid_to = timezone.now())
      return redirect('released')
  
  else:
    form = TurtleDeleteForm()
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': released_act,
    'about_act': '',
    'current_act': current_act,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7)),
    'form': form,
    'turtle' : Turtle.objects.get(valid_to = None, id = id),
  }

  return render(request, 'turtles/TurtleDelete.html', context)

def Confirm(request, username):
  confirmation = request.session.get('confirmation')
  if request.method == 'POST':
    form = UserConfirmationForm(request.POST)
    if form.is_valid():
      if form.cleaned_data["code"] == confirmation:
        User.objects.filter(username = username).update(is_active = True)
        return redirect('login')
      else:
        return redirect('signup')
  else:
    form = UserConfirmationForm()
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'form': form,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'registration/confirm.html', context)

def SignUp(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)  
      user.is_active = False  
      user.save()
      confirmation = random.randint(10000, 99999)
      yag = yagmail.SMTP('terrapintrackercontact@gmail.com', oauth2_file = "./oauth2_creds.json")
      yag.send(to = [user.email], subject = 'Terrapin Tracker Email Confirmation', contents = 'Your confirmation number is: ' + str(confirmation))
      request.session['confirmation'] = confirmation
      return redirect('confirm', user.username)
  else:
    form = UserRegisterForm()
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'form': form,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'registration/signup.html', context)

def search(request):
  if request.method == 'POST':
    form = NewSearchForm(request.POST)
    if form.is_valid():
      if request.POST.get('archived'):
        return redirect('current_r', year_archived=request.POST.get('year_archived'), r_num=request.POST.get('r_num'))
      else:
        return redirect('current_r', year_archived=0, r_num=request.POST.get('r_num'))
  
  else:
    form = NewSearchForm()

  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'form': form,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/search.html', context)

def send_current_file(request):
  with open('./turtles/static/turtles/current_measurements.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['R Number', 'Hatchling Number', 'Archived', 'Year Archived', 'Date','Carapace Length', 'Carapace Width', 'Plastron Length', 'Carapace Height', 'Mass'])
    values = Measurement.objects.filter(valid_to = None, turtle__archived = False).values_list('turtle', 'date', 'carapace_length', 'carapace_width', 'plastron_length', 'carapace_height', 'mass')
    correct_values = []
    number = 0
    for x in values:
      correct_values.append([])
      one_time = True
      correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].r_num)
      correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].hatchling_num)
      correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].archived)
      if Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].archived:
        correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].year_archived)
      else:
        correct_values[number].append('')
      for y in x:
        if one_time:
          one_time = False
          continue
        correct_values[number].append(y)
      number += 1
    for value in correct_values:
      writer.writerow(value)
  csvfile.close()
  
  filename = './turtles/static/turtles/current_measurements.csv'
  download_name = 'current_measurements.csv'
  wrapper = FileWrapper(open(filename))
  response = HttpResponse(wrapper,content_type='text/csv')
  response['Content-Disposition'] = "attachment; filename=%s"%download_name
  return response

def send_archived_file(request):
  with open('./turtles/static/turtles/archived_measurements.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['R Number', 'Hatchling Number', 'Archived', 'Year Archived', 'Date','Carapace Length', 'Carapace Width', 'Plastron Length', 'Carapace Height', 'Mass'])
    values = Measurement.objects.filter(valid_to = None, turtle__archived = True).values_list('turtle', 'date', 'carapace_length', 'carapace_width', 'plastron_length', 'carapace_height', 'mass')
    correct_values = []
    number = 0
    for x in values:
      correct_values.append([])
      one_time = True
      correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].r_num)
      correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].hatchling_num)
      correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].archived)
      if Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].archived:
        correct_values[number].append(Turtle.objects.filter(id = int(x[0]), valid_to = None)[0].year_archived)
      else:
        correct_values[number].append('')
      for y in x:
        if one_time:
          one_time = False
          continue
        correct_values[number].append(y)
      number += 1
    for value in correct_values:
      writer.writerow(value)
  csvfile.close()
  
  filename = './turtles/static/turtles/archived_measurements.csv'
  download_name = 'archived_measurements.csv'
  wrapper = FileWrapper(open(filename))
  response = HttpResponse(wrapper,content_type='text/csv')
  response['Content-Disposition'] = "attachment; filename=%s"%download_name
  return response

def custom_page_not_found_view(request, exception):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }
  
  return render(request, "turtles/404.html", context)

def custom_error_view(request, exception=None):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }
  
  return render(request, "turtles/500.html", context)

def custom_permission_denied_view(request, exception=None):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }
  
  return render(request, "turtles/403.html", context)

def custom_bad_request_view(request, exception=None):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }
  
  return render(request, "turtles/400.html", context)

def home(request, alert = 1):
  
  measurements = []
  for i in Measurement.objects.filter(valid_to = None):
    if i.turtle.archived == False:
      measurements.append(i)


  date = []
  for measurement in Measurement.objects.filter(valid_to = None):
      date.append(measurement.date)
  group = []
  for measurement in Measurement.objects.filter(valid_to = None):
      group.append((measurement.display_turtle.split('-')[0]))
  
  carapace_length = []
  for measurement in Measurement.objects.filter(valid_to = None):
      carapace_length.append(measurement.carapace_length)
  
  carapace_width = []
  for measurement in Measurement.objects.filter(valid_to = None):
      carapace_width.append(measurement.carapace_width)
  
  plastron_length = []
  for measurement in Measurement.objects.filter(valid_to = None):
      plastron_length.append(measurement.plastron_length)
  
  carapace_height = []
  for measurement in Measurement.objects.filter(valid_to = None):
      carapace_height.append(measurement.carapace_height)
  
  mass = []
  for measurement in Measurement.objects.filter(valid_to = None):
      mass.append(measurement.mass)
  
  fig, ax = plt.subplots()
  legend = (list(set(group)))
  try:
    legend = sorted([int(x) for x in legend])
  except:
    print(legend)
  legend = ([str(x) for x in legend])
  sns_plot = sns.scatterplot(ax=ax, x=carapace_length, y=carapace_width, hue=group, hue_order = legend).set_title('Carapace Length vs Carapace Width')
  ax.set_xlabel( "Carapace Length" , size = 12 )
  ax.set_ylabel( "Carapace Width" , size = 12 )
  plt.legend(title='R Group', loc='lower right')
  file_path = './turtles/static/turtles/plot_r' + 'lengthvswidthhomescatter.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.kdeplot(ax=ax, x=carapace_length, y=carapace_width, fill=True, cmap="crest").set_title('Carapace Length vs Carapace Width')
  ax.set_xlabel( "Carapace Length" , size = 12 )
  ax.set_ylabel( "Carapace Width" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + 'lengthvswidthhomekde.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.boxplot(ax=ax, x=date, y=carapace_length, palette='Blues', showfliers=False).set_title('Carapace Length over Time')
  ax.set_xlabel( "Measurement Date" , size = 12 )
  ax.set_ylabel( "Carapace Length" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + 'datevslengthhomebox.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  legend = (list(set(group)))
  legend = sorted([int(x) for x in legend])
  legend = ([str(x) for x in legend])
  sns_plot = sns.scatterplot(ax=ax, x=plastron_length, y=carapace_height, hue=group, hue_order=legend).set_title('Plastron Length vs Carapace Height')
  ax.set_xlabel( "Plastron Length" , size = 12 )
  ax.set_ylabel( "Carapace Height" , size = 12 )
  plt.legend(title='R Group', loc='lower right')
  file_path = './turtles/static/turtles/plot_r' + 'lengthvsheighthomescatter.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sns_plot = sns.kdeplot(ax=ax, x=plastron_length, y=carapace_height, fill=True, cmap='crest').set_title('Plastron Length vs Carapace Height')
  ax.set_xlabel( "Plastron Length" , size = 12 )
  ax.set_ylabel( "Carapace Height" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + 'lengthvsheighthomekde.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()
  
  fig, ax = plt.subplots()
  sns_plot = sns.boxplot(ax=ax, x=date, y=carapace_height, palette='Blues', showfliers=False).set_title('Carapace Height over Time')
  ax.set_xlabel( "Measurement Date" , size = 12 )
  ax.set_ylabel( "Carapace Height" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + 'datevsheighthomebox.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  
  fig, ax = plt.subplots()
  sortgroup = sorted([int(x) for x in group])
  sortgroup = ([str(x) for x in sortgroup])
  sns_plot = sns.barplot(ax=ax, x=sortgroup, y=carapace_length, palette='light:orange').set_title('Carapace Length by R Group')
  ax.set_xlabel( "R Group" , size = 12 )
  ax.set_ylabel( "Carapace Length" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + 'rvslengthbar.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sortgroup = sorted([int(x) for x in group])
  sortgroup = ([str(x) for x in sortgroup])
  sns_plot = sns.barplot(ax=ax, x=sortgroup, y=carapace_width, palette='light:orange').set_title('Carapace Width by R Group')
  ax.set_xlabel( "R Group" , size = 12 )
  ax.set_ylabel( "Carapace Width" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + 'rvswidthbar.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()

  fig, ax = plt.subplots()
  sortgroup = sorted([int(x) for x in group])
  sortgroup = ([str(x) for x in sortgroup])
  sns_plot = sns.barplot(ax=ax, x=sortgroup, y=carapace_height, palette='light:orange').set_title('Carapace Height by R Group')
  ax.set_xlabel( "R Group" , size = 12 )
  ax.set_ylabel( "Carapace Height" , size = 12 )
  file_path = './turtles/static/turtles/plot_r' + 'rvsheightbar.png'
  fig = sns_plot.get_figure()
  fig.savefig(file_path)
  plt.clf()




  path9 = 'turtles/plot_r' + 'lengthvswidthhomescatter.png'
  path10 = 'turtles/plot_r' + 'lengthvswidthhomekde.png'
  path11 = 'turtles/plot_r' + 'datevslengthhomebox.png'
  path12 = 'turtles/plot_r' + 'lengthvsheighthomescatter.png'
  path13 = 'turtles/plot_r' + 'lengthvsheighthomekde.png'
  path14 = 'turtles/plot_r' + 'datevsheighthomebox.png'
  path15 = 'turtles/plot_r' + 'rvslengthbar.png'
  path16 = 'turtles/plot_r' + 'rvswidthbar.png'
  path17 = 'turtles/plot_r' + 'rvsheightbar.png'





  context= {
    'home_act': 'active',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'Turtle': Turtle.objects.filter(archived = False, valid_to = None),
    'Measurement' : measurements,
    'path9' : path9,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7)),
    'path10' : path10,
    'path11' : path11,
    'path12' : path12,
    'path13' : path13,
    'path14' : path14,
    'path15' : path15,
    'path16' : path16,
    'path17' : path17,
    'alert' : alert,
  }

  return render(request, 'turtles/home.html', context)

def contact(request):
  if request.method == 'POST':
    form = NewContactForm(request.POST)
    
    if form.is_valid():
      emails = []
      for i in User.objects.filter(is_superuser = True):
        emails.append(i.email)
      yag = yagmail.SMTP('terrapintrackercontact@gmail.com', oauth2_file = "./oauth2_creds.json")
      yag.send(to = emails, subject = str(form.cleaned_data["subject"]), contents = 'From:\n' + str(form.cleaned_data["email"]) + '\n\nMessage:\n' + str(form.cleaned_data["body"]))

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
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/contact.html', context)

def contactsent(request):
  context = {
    'home_act': '',
    'contact_act': 'active',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/contactsent.html', context)

def released(request):
  measurements = []
  for i in Measurement.objects.filter(valid_to = None):
    if i.turtle.archived == True:
      measurements.append(i)
  
  r_nums = set()
  for x in Turtle.objects.filter(archived = True, valid_to = None):
    r_nums.add((x.r_num, x.year_archived))
  r_nums = list(r_nums)
  r_nums = sorted(r_nums, key = lambda x: x[0])
  
  years = []
  for i in Turtle.objects.filter(archived = True, valid_to = None).values('year_archived').distinct():
    years.append(i['year_archived'])
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': 'active',
    'about_act': '',
    'current_act': '',
    'Turtle': Turtle.objects.filter(archived = True, valid_to = None),
    'Measurement' : measurements,
    'r_nums' : r_nums,
    'years' : years,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/released.html', context)

def about(request):
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': 'active',
    'current_act': '',
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/about.html', context)

def current(request):
  measurements = []
  for i in Measurement.objects.filter(valid_to = None):
    if i.turtle.archived == False:
      measurements.append(i)

  r_nums = []
  for x in Turtle.objects.filter(valid_to = None).values('r_num').distinct():
    include = False
    for y in Turtle.objects.filter(r_num = x['r_num'], valid_to = None):
      if (y.archived == False):
        include = True
    if include:
      r_nums.append(x['r_num'])
  r_nums = sorted([x for x in r_nums])


  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': 'active',
    'Turtle': Turtle.objects.filter(archived = False, valid_to = None),
    'Measurement' : measurements,
    'r_nums' : r_nums,
    'year_archived' : 0,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/current.html', context)

@login_required
def current_r_deleted(request, year_archived, r_num, year_deleted):
  no_turtles = True
  for measurement in Measurement.objects.exclude(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived and measurement.turtle.valid_to.year == year_deleted:
      no_turtles = False

  context = {
    'no_turtles' : no_turtles,
    'home_act': '',
    'contact_act': '',
    'released_act': 'active',
    'about_act': '',
    'current_act': '',
    'Turtle': Turtle.objects.exclude(valid_to = None),
    'Measurement' : Measurement.objects.exclude(valid_to = None).order_by('date'),
    'r' : r_num,
    'year_archived': year_archived,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7)),
    'year_deleted': year_deleted,
  }

  return render(request, 'turtles/current_r_deleted.html', context)

def current_r(request, year_archived, r_num):
  no_turtles = True
  for measurement in Measurement.objects.filter(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      no_turtles = False
  
  current_act = ''
  released_act = ''
  if year_archived == 0:
    current_act = 'active'
  else:
    released_act = 'active'
  
  unique_turtles = set()
  for turtle in Turtle.objects.filter(valid_to = None, r_num = r_num, year_archived = year_archived):
    unique_turtles.add(turtle)

  def getR(obj):
    return obj.r_num
  
  def getHatch(obj):
    return obj.hatchling_num
  
  unique_turtles = sorted(list(unique_turtles), key=getHatch)
  unique_turtles = sorted(list(unique_turtles), key=getR)

  if no_turtles:
    context = {
      'no_turtles' : no_turtles,
      'home_act': '',
      'contact_act': '',
      'released_act': released_act,
      'about_act': '',
      'current_act': current_act,
      'Turtle': Turtle.objects.filter(valid_to = None),
      'Measurement' : Measurement.objects.filter(valid_to = None).order_by('date'),
      'r' : r_num,
      'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7)),
      'unique_turtles': unique_turtles,
    }

    return render(request, 'turtles/current_r.html', context)

  date = []
  for measurement in Measurement.objects.filter(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      date.append(measurement.date)
  
  turtle = []
  for measurement in Measurement.objects.filter(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      turtle.append(measurement.display_turtle.split('-')[1])
  
  carapace_length = []
  for measurement in Measurement.objects.filter(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_length.append(measurement.carapace_length)
  
  carapace_width = []
  for measurement in Measurement.objects.filter(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_width.append(measurement.carapace_width)
  
  plastron_length = []
  for measurement in Measurement.objects.filter(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      plastron_length.append(measurement.plastron_length)
  
  carapace_height = []
  for measurement in Measurement.objects.filter(valid_to = None):
    if measurement.turtle.r_num == r_num and measurement.turtle.year_archived == year_archived:
      carapace_height.append(measurement.carapace_height)
  
  mass = []
  for measurement in Measurement.objects.filter(valid_to = None):
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
  file_path = './turtles/static/turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'datevslengthbox.png'
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
  sns_plot = sns.histplot(ax=ax, x=mass, bins='auto').set_title('Turtle Mass Distribution')
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

  path1 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvswidthscatter.png'
  path2 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'lengthvswidthkde.png'
  path3 = 'turtles/plot_r' + str(r_num) + 'year' + str(year_archived) + 'datevslengthbox.png'
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
    'Turtle': Turtle.objects.filter(valid_to = None),
    'Measurement' : Measurement.objects.filter(valid_to = None).order_by('date'),
    'r' : r_num,
    'year_archived' : year_archived,
    'path1' : path1,
    'path2' : path2,
    'path3' : path3,
    'path4' : path4,
    'path5' : path5,
    'path6' : path6,
    'path7' : path7,
    'path8' : path8,
    'path9' : path9,
    'unique_turtles': unique_turtles,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'turtles/current_r.html', context)

def userlogin(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password'],
      )
      if user is not None:
        login(request, user)
        return redirect('home')

  else:
    form = LoginForm()
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'form' : form,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'registration/login.html', context)

class TurtleCreate(LoginRequiredMixin, CreateView):
  model = Turtle
  form_class = NewTurtleCreateForm
  template_name = 'turtles/newturtlecreateform.html'
  success_url = '/current/'

  def get_initial(self):
    return {'editor':self.request.user.first_name + ' ' + self.request.user.last_name + ' (' + self.request.user.email + ')'}

class MeasurementCreate(LoginRequiredMixin, CreateView):
  model = Measurement
  form_class = NewMeasurementCreateForm
  template_name = 'turtles/newmeasurementcreateform.html'
  success_url = '/current/'
  
  def get_initial(self):
    return {'editor':self.request.user.first_name + ' ' + self.request.user.last_name + ' (' + self.request.user.email + ')', 'date': timezone.now}

def logout_request(request):
  logout(request)
  return redirect("home")

def forgot(request):
  if request.method == 'POST':
    form = ForgotForm(request.POST)
    if form.is_valid():
      raw_password = ''.join(random.choices(string.ascii_letters, k=8)) + ''.join(random.choices(string.punctuation, k=2))
      user = User.objects.get(email = form.cleaned_data['email'], is_active = True)
      user.set_password(raw_password)
      user.save()
      yag = yagmail.SMTP('terrapintrackercontact@gmail.com', oauth2_file = "./oauth2_creds.json")
      yag.send(to = [form.cleaned_data['email']], subject = 'Terrapin Tracker Username and Password Retrieval', contents = 'Your username is: ' + user.username + '\n\nYour new password is: ' + raw_password)
      return redirect('login')

  else:
    form = ForgotForm()
  
  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'form' : form,
    'confirmation': ''.join(random.choices(string.ascii_uppercase, k=7))
  }

  return render(request, 'registration/forgot.html', context)

@login_required
def settings(request, confirmation):
  delete = NewDeleteForm()
  name = ChangeNameForm()
  password = ChangePassword()

  if request.method == 'POST':
    if 'delete' in request.POST:
      delete = NewDeleteForm(request.POST)
      if delete.is_valid():
        if delete.cleaned_data["confirmation"] == confirmation:
          User.objects.filter(username = request.user.get_username()).update(is_active = False)
          return redirect("home")
        else:
          return redirect("settings", ''.join(random.choices(string.ascii_uppercase, k=7)))
    elif 'name' in request.POST:
      name = ChangeNameForm(request.POST)
      if name.is_valid():
        User.objects.filter(username = request.user.get_username()).update(first_name = name.cleaned_data["first_name"])
        User.objects.filter(username = request.user.get_username()).update(last_name = name.cleaned_data["last_name"])
        return redirect("settings", ''.join(random.choices(string.ascii_uppercase, k=7)))
    elif 'password' in request.POST:
      password = ChangePassword(request.POST)
      if password.is_valid():
        user = authenticate(
          username = request.user.get_username(),
          password = password.cleaned_data['old_password'],
        )
        if user is not None:
          user.set_password(password.cleaned_data['password1'])
          user.save()
          return redirect("settings", ''.join(random.choices(string.ascii_uppercase, k=7)))          

  context = {
    'home_act': '',
    'contact_act': '',
    'released_act': '',
    'about_act': '',
    'current_act': '',
    'delete': delete,
    'name': name,
    'password': password,
    'confirmation': confirmation,
  }

  return render(request, 'turtles/settings.html', context)