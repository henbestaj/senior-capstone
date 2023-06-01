# ****************************************************************************
#   File Name: forms.py
#   Purpose:
#     * Create the forms that are needed as a part of the turtles app
#     * Create the fields for each forms as well as parameters on each field
#     * Create error messages for each form as needed
# ****************************************************************************

# Import statements
from django import forms
from .models import Turtle, Measurement
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone, dateformat

# Create a form to let the user confirm they want to delete a turtle
class TurtleDeleteForm(forms.Form):
  # Create the field for this form as well as parameters on the field
  confirm = forms.BooleanField(label="Confirm you want to delete this turtle:")

# Create a form to let the user confirm they want to delete a measurement
class MeasurementDeleteForm(forms.Form):
  # Create the field for this form as well as parameters on the field
  confirm = forms.BooleanField(label="Confirm you want to delete this measurement:")

# Create a form to let the user archive many turtles or R groups at once
class MassArchiveForm(forms.Form):
  # Create error messages for this form
  def clean(self):
    # Grab the data that is needed from the form to find the errors
    data = self.cleaned_data
    r_num_field = data['r_num_field']
    individual_turtles = data['individual_turtles']

    # Create an error for when a similar turtle has already been archived
    for i in individual_turtles:
      if Turtle.objects.filter(r_num = Turtle.objects.get(id = i).r_num, hatchling_num = Turtle.objects.get(id = i).hatchling_num, archived = True, year_archived = int(dateformat.format(timezone.now(), 'Y'))).exists():
        raise forms.ValidationError('One of these turtles already exists.')
    
    # Create an error for when in the R group being archived there is a turtle that is similar to a turtle that has already been archived
    for i in r_num_field:
      for x in Turtle.objects.filter(valid_to = None, archived = False, r_num = i):
        if Turtle.objects.filter(r_num = i, hatchling_num = x.hatchling_num, archived = True, year_archived = int(dateformat.format(timezone.now(), 'Y'))).exists():
          raise forms.ValidationError('One of these turtles already exists.')

  # Create a list of all the R numbers currently active
  r_nums = []
  for x in Turtle.objects.filter(valid_to = None).values('r_num').distinct():
    include = False
    for y in Turtle.objects.filter(r_num = x['r_num'], valid_to = None):
      if (y.archived == False):
        include = True
    if include:
      r_nums.append(x['r_num'])
  r_nums = sorted([x for x in r_nums])
  
  # Change the list of all the R numbers currently active to a list of tuples
  r_tuples = []
  for i in r_nums:
    r_tuples.append((i, i))
  
  # Create a list of tuples of all the turtles currently active
  turtles = []
  for i in Turtle.objects.filter(valid_to = None, archived = False):
    turtles.append((i.id, i))
  
  # Create the fields for this form as well as parameters on the fields
  r_num_field = forms.MultipleChoiceField(label = 'Full R Groups', required=False, choices=r_tuples, widget=forms.CheckboxSelectMultiple)
  individual_turtles = forms.MultipleChoiceField(label = 'Individual Turtles', required=False, choices=turtles, widget=forms.CheckboxSelectMultiple)

  # Override the default __init__ function to allow the R numbers list and turtles list to automatically update every time the form is loaded in
  def __init__(self, *args, **kwargs):
    super(MassArchiveForm, self).__init__(*args, **kwargs)
    
    # Create a list of all the R numbers currently active
    r_nums = []
    for x in Turtle.objects.filter(valid_to = None).values('r_num').distinct():
      include = False
      for y in Turtle.objects.filter(r_num = x['r_num'], valid_to = None):
        if (y.archived == False):
          include = True
      if include:
        r_nums.append(x['r_num'])
    r_nums = sorted([x for x in r_nums])
    
    # Change the list of all the R numbers currently active to a list of tuples
    r_tuples = []
    for i in r_nums:
      r_tuples.append((i, i))
    
    # Create a list of tuples of all the turtles currently active
    turtles = []
    for i in Turtle.objects.filter(valid_to = None, archived = False):
      turtles.append((i.id, i))
    
    # Update the choices for the r_num_field and individual_turtles fields
    self.fields['r_num_field'].choices = r_tuples
    self.fields['individual_turtles'].choices = turtles

# Create a form to let the user sign up
class UserRegisterForm(UserCreationForm):
  # Override the default password_mismatch error
  error_messages = {
    'password_mismatch': 'Passwords do not match.',
  }
  
  # Create error messages for this form
  def clean(self):
    # Grab the data that is needed from the form to find the errors
    data = self.cleaned_data
    email = data['email']
    username = data['username']

    # Create an error for when the username and email entered has already been used and they didn't use an ocvts email
    if User.objects.filter(username = username).exists() == True and User.objects.filter(email = email, is_active = True).exists() == True and 'ocvts.org' not in email:
      raise forms.ValidationError("The username and email you entered are already in use. Additionally, please use your ocvts.org email.")
    
    # Create an error for when the username and email entered has already been used
    if User.objects.filter(username = username).exists() == True and User.objects.filter(email = email, is_active = True).exists() == True:
      raise forms.ValidationError("The username and email you entered are already in use.")
    
    # Create an error for when the username entered has already been used and they didn't use an ocvts email
    if User.objects.filter(username = username).exists() == True and 'ocvts.org' not in email:
      raise forms.ValidationError("The username you entered is already in use. Additionally, please use your ocvts.org email.")
    
    # Create an error for when the email entered has already been used and they didn't use an ocvts email
    if User.objects.filter(email = email, is_active = True).exists() == True and 'ocvts.org' not in email:
      raise forms.ValidationError("The email you entered is already in use. Additionally, please use your ocvts.org email.")
    
    # Create an error for when the username entered has already been used
    if User.objects.filter(username = username).exists() == True:
      raise forms.ValidationError("The username you entered is already in use.")
    
    # Create an error for when the email entered has already been used
    if User.objects.filter(email = email, is_active = True).exists() == True:
      raise forms.ValidationError("The email you entered is already in use.")
    
    # Create an error for when they didn't use an ocvts email
    if 'ocvts.org' not in email:
      raise forms.ValidationError("Please use your ocvts.org email.")
  
  # Create the fields for this form as well as parameters on the fields
  email = forms.EmailField(label = 'Email', help_text='Please use your ocvts.org email.')
  first_name = forms.CharField(label = 'First Name')
  last_name = forms.CharField(label = 'Last Name')
  username = forms.CharField(label = 'Username')
  password1 = forms.CharField(widget = forms.PasswordInput, label = 'Password')
  password2 = forms.CharField(widget = forms.PasswordInput, label = 'Password Confirmation', help_text='Enter the same password as before, for verification.')
  
  # Corrects the password mismatch error
  def clean_password_confirm(self):
    # Grab the data that is needed from the form to find the error
    password = self.cleaned_data['password1']
    password_confirm = self.cleaned_data.get('password2')

    # Create an error for when passwords do not match
    if password and password_confirm:
      if password != password_confirm:
        raise forms.ValidationError("")
  
  # Establish the metadata for the form
  class Meta:
    # Establish the model associated with the form
    model = User

    # Establish the fields from the model needed in the form
    fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2']

# Create a form to let the user change their password
class ChangePassword(forms.Form):
  # Create an error message for this form
  def clean(self):
    # Grab the data that is needed from the form to find the error
    data = self.cleaned_data
    password1 = data['password1']
    password2 = data['password2']

    # Create an error for when passwords do not match
    if password1 != password2:
      raise forms.ValidationError("Passwords do not match.")
  
  # Create the fields for this form as well as parameters on the fields
  old_password = forms.CharField(widget = forms.PasswordInput, label = 'Old Password')
  password1 = forms.CharField(widget = forms.PasswordInput, label = 'New Password')
  password2 = forms.CharField(widget = forms.PasswordInput, label = 'New Password Confirmation', help_text='Enter the same password as before, for verification.<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>')
  password = forms.BooleanField(widget=forms.HiddenInput, initial=True)

# Create a form to let the user edit a turtle when the turtle is archived
class EditTurtleCreateFormArchived(forms.Form):
  # Create error messages for this form
  def clean(self):
    # Grab the data that is needed from the form to find the errors
    data = self.cleaned_data
    id = data['id']
    r_num = data['r_num']
    hatchling_num = data['hatchling_num']
    year_archived = data['year_archived']

    # Create an error for when the R number is below zero
    if r_num < 0:
      raise forms.ValidationError('Ensure the R number is greater than or equal to 0.')
  
    # Create an error for when the hatchling number is below zero
    if hatchling_num < 0:
      raise forms.ValidationError('Ensure the hatchling number is greater than or equal to 0.')

    # Create an error for when the turtle already exists
    if Turtle.objects.exclude(id = id).filter(valid_to = None, r_num = r_num, hatchling_num = hatchling_num, year_archived = year_archived).exists():
      raise forms.ValidationError('This turtle already exists.')

  # Create the fields for this form as well as parameters on the fields
  r_num = forms.IntegerField(label = 'R Number')
  hatchling_num = forms.IntegerField(label = 'Hatchling Number')
  archived = forms.BooleanField(required=False, label = 'Archived', widget=forms.CheckboxInput(attrs={'checked': ''}))
  year_archived = forms.IntegerField(widget = forms.HiddenInput())
  id = forms.IntegerField(widget = forms.HiddenInput())

# Create a form to let the user edit a measurement
class EditMeasurementCreateForm(forms.Form):
  # Create error messages for this form
  def clean(self):
    # Grab the data that is needed from the form to find the errors
    data = self.cleaned_data
    carapace_length = data['carapace_length']
    carapace_width = data['carapace_width']
    plastron_length = data['plastron_length']
    carapace_height = data['carapace_height']
    mass = data['mass']

    # Create an error for when the carapace length is below zero
    if carapace_length < 0:
      raise forms.ValidationError('Ensure the carapace length is greater than or equal to 0.')

    # Create an error for when the carapace width is below zero
    if carapace_width < 0:
      raise forms.ValidationError('Ensure the carapace width is greater than or equal to 0.')

    # Create an error for when the plastron length is below zero
    if plastron_length < 0:
      raise forms.ValidationError('Ensure the plastron length is greater than or equal to 0.')
    
    # Create an error for when the carapace height is below zero
    if carapace_height < 0:
      raise forms.ValidationError('Ensure the carapace height is greater than or equal to 0.')
    
    # Create an error for when the mass is below zero
    if mass < 0:
      raise forms.ValidationError('Ensure the mass is greater than or equal to 0.')
  
  # Create the fields for this form as well as parameters on the fields
  date = forms.DateField(label = 'Date (YYYY-MM-DD)')
  carapace_length = forms.FloatField(label = 'Carapace Length (mm)')
  carapace_width = forms.FloatField(label = 'Carapace Width (mm)')
  plastron_length = forms.FloatField(label = 'Plastron Length (mm)')
  carapace_height = forms.FloatField(label = 'Carapace Height (mm)')
  mass = forms.FloatField(label = 'Mass (g)')
  turtle = forms.ModelChoiceField(queryset = Turtle.objects.all().filter(valid_to=None, archived=False), label = 'Turtle')
  id = forms.IntegerField(widget = forms.HiddenInput())

  # Override the default __init__ function to allow the turtles list to automatically update every time the form is loaded in
  def __init__(self, *args, **kwargs):
    super(EditMeasurementCreateForm, self).__init__(*args, **kwargs)

    # Update the choices for the turtle field
    self.fields['turtle'].queryset = Turtle.objects.all().filter(valid_to=None, archived=False)

# Create a form to let the user edit a turtle when the turtle is not archived
class EditTurtleCreateForm(forms.Form):
  # Create error messages for this form
  def clean(self):
    # Grab the data that is needed from the form to find the errors
    data = self.cleaned_data
    id = data['id']
    r_num = data['r_num']
    hatchling_num = data['hatchling_num']
    year_archived = data['year_archived']

    # Create an error for when the R number is below zero
    if r_num < 0:
      raise forms.ValidationError('Ensure the R number is greater than or equal to 0.')
  
    # Create an error for when the hatchling number is below zero
    if hatchling_num < 0:
      raise forms.ValidationError('Ensure the hatchling number is greater than or equal to 0.')

    # Create an error for when the turtle already exists
    if Turtle.objects.exclude(id = id).filter(valid_to = None, r_num = r_num, hatchling_num = hatchling_num, year_archived = year_archived).exists():
      raise forms.ValidationError('This turtle already exists.')

  # Create the fields for this form as well as parameters on the fields
  r_num = forms.IntegerField(label = 'R Number')
  hatchling_num = forms.IntegerField(label = 'Hatchling Number')
  archived = forms.BooleanField(required=False, label = 'Archived')
  year_archived = forms.IntegerField(widget = forms.HiddenInput())
  id = forms.IntegerField(widget = forms.HiddenInput())

# Create a form to let the user create a new turtle
class NewTurtleCreateForm(forms.ModelForm):
  # Create error message for this form
  def clean(self):
    # Grab the data that is needed from the form to find the error
    data = self.cleaned_data
    r_num = data['r_num']
    hatchling_num = data['hatchling_num']

    # Create an error for when the turtle being created already exists
    if Turtle.objects.filter(archived = False, r_num = r_num, hatchling_num = hatchling_num, valid_to = None).exists():
      raise forms.ValidationError("This turtle already exists.")
    
    return data
  
  # Create the field for this form as well as parameters on the field
  editor = forms.CharField(widget=forms.HiddenInput)

  # Establish the metadata for the form
  class Meta:
    # Establish the model associated with the form
    model = Turtle

    # Establish the fields from the model needed in the form
    fields = ['r_num', 'hatchling_num', 'editor']
  
class MassTurtleCreateForm(forms.Form):
  r_num1 = forms.IntegerField(label = 'Starting R Number')
  r_num2 = forms.IntegerField(label = 'Ending R Number')
  hatchling_num1 = forms.IntegerField(label = 'Starting Hatchling Number')
  hatchling_num2 = forms.IntegerField(label = 'Ending Hatchling Number')
  editor = forms.CharField(widget=forms.HiddenInput)
  
  def clean(self):
    data = self.cleaned_data
    r_num1 = data['r_num1']
    r_num2 = data['r_num2']
    hatchling_num1 = data['hatchling_num1']
    hatchling_num2 = data['hatchling_num2']

    if r_num1 > r_num2:
      raise forms.ValidationError("Please ensure the ending R number is above the starting R number.")
    
    if hatchling_num1 > hatchling_num2:
      raise forms.ValidationError("Please ensure the ending hatchling number is above the starting hatchling number.")

    for x in range(r_num1, r_num2 + 1):
      for y in range(hatchling_num1, hatchling_num2 + 1):
        if Turtle.objects.filter(archived = False, r_num = x, hatchling_num = y, valid_to = None).exists():
          raise forms.ValidationError("One of these turtles already exists.")
    
    return data

class NewMeasurementCreateForm(forms.ModelForm):
  editor = forms.CharField(widget=forms.HiddenInput)
  date = forms.DateField(label = 'Date (YYYY-MM-DD)')
  
  def __init__(self, *args, **kwargs):
    super(NewMeasurementCreateForm, self).__init__(*args, **kwargs)
    self.fields['turtle'].queryset = Turtle.objects.all().filter(valid_to=None, archived=False)

  class Meta:
    model = Measurement
    fields = ['turtle','date', 'carapace_length', 'carapace_width', 'carapace_height', 'plastron_length', 'mass', 'editor']

# Create a form to let the user send an email to all superusers
class NewContactForm(forms.Form):
  # Create the fields for this form as well as parameters on the fields
  email = forms.EmailField(label = 'Your Email')
  subject = forms.CharField(label = 'Subject')
  body = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label='Body')

# Create a form to let the user search for turtles
class NewSearchForm(forms.Form):  
  # Create the error message for this form
  def clean(self):
    # Grab the data that is needed from the form to find the error
    data = self.cleaned_data
    archived = data['archived']
    year_archived = data['year_archived']

    # Create an error for when the user enters that the turtle is archived but doesn't include a year archived
    if archived and not year_archived:
      raise forms.ValidationError("Please enter a year archived when searching for archived turtles.")
  
  # Create the fields for this form as well as parameters on the fields
  r_num = forms.IntegerField(label = 'R Number')
  archived = forms.BooleanField(required=False, label = 'Archived?')
  year_archived = forms.IntegerField(required=False, label = 'Year Archived')

# Create a form to let the user confirm their email address
class UserConfirmationForm(forms.Form):
  # Create the field for this form as well as parameters on the field
  code = forms.IntegerField(label='Confirmation Code', validators=[MaxValueValidator(99999), MinValueValidator(10000)])

# Create a form to let the user delete their account
class NewDeleteForm(forms.Form):
  # Create the fields for this form as well as parameters on the fields
  confirmation = forms.CharField(label = 'Type the letters above to confirm account deletion')
  delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)

# Create a form to let the user retrieve their username and password if they forgot them
class ForgotForm(forms.Form):
  # Create the field for this form as well as parameters on the field
  email = forms.EmailField(label = 'Email', help_text='Please use your ocvts.org email.')

  # Create the error message for this form
  def clean(self):
    # Grab the data that is needed from the form to find the error
    data = self.cleaned_data
    email = data['email']

    # Create an error for when the user doesn't exist
    if not User.objects.filter(email = email, is_active = True).exists():
      raise forms.ValidationError("This user does not exist.")

# Create a form to let the user change their name
class ChangeNameForm(forms.Form):
  # Create the fields for this form as well as parameters on the fields
  first_name = forms.CharField(label = 'First Name')
  last_name = forms.CharField(label = 'Last Name')
  name = forms.BooleanField(widget=forms.HiddenInput, initial=True)

# Create a form to let the user login
class LoginForm(forms.Form):
  # Create the error message for this form
  def clean(self):
    # Grab the data that is needed from the form to find the error
    data = self.cleaned_data
    username = data['username']

    # Create an error for when the user doesn't exist
    if User.objects.filter(username = username).exists() == False:
      raise forms.ValidationError("Please enter a correct username.")
  
  # Create the fields for this form as well as parameters on the fields
  username = forms.CharField(label='Username')
  password = forms.CharField(label='Password', widget = forms.PasswordInput)