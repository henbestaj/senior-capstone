from django import forms
from .models import Turtle, Measurement
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator

# Inherit Django's default UserCreationForm
class UserRegisterForm(UserCreationForm):
  error_messages = {
        'password_mismatch': 'Passwords do not match.',
        
    }
  def clean(self):
    data = self.cleaned_data
    email = data['email']
    username = data['username']

    # user, email, ocvts
    if User.objects.filter(username = username).exists() == True and User.objects.filter(email = email, is_active = True).exists() == True and 'ocvts.org' not in email:
      raise forms.ValidationError("The username and email you entered are already in use. Additionally, please use your ocvts.org email.")
    # email and user
    if User.objects.filter(username = username).exists() == True and User.objects.filter(email = email, is_active = True).exists() == True:
      raise forms.ValidationError("The username and email you entered are already in use.")
    # user and ocvts
    if User.objects.filter(username = username).exists() == True and 'ocvts.org' not in email:
      raise forms.ValidationError("The username you entered is already in use. Additionally, please use your ocvts.org email.")
    # email and ocvts
    if User.objects.filter(email = email, is_active = True).exists() == True and 'ocvts.org' not in email:
      raise forms.ValidationError("The email you entered is already in use. Additionally, please use your ocvts.org email.")
    # user
    if User.objects.filter(username = username).exists() == True:
      raise forms.ValidationError("The username you entered is already in use.")
    # email
    if User.objects.filter(email = email, is_active = True).exists() == True:
      raise forms.ValidationError("The email you entered is already in use.")
    # ocvts
    if 'ocvts.org' not in email:
      raise forms.ValidationError("Please use your ocvts.org email.")
    
  
  email = forms.EmailField(label = 'Email', help_text='Please use your ocvts.org email.')
  first_name = forms.CharField(label = 'First Name')
  last_name = forms.CharField(label = 'Last Name')
  username = forms.CharField(label = 'Username')
  password1 = forms.CharField(widget = forms.PasswordInput, label = 'Password')
  password2 = forms.CharField(widget = forms.PasswordInput, label = 'Password Confirmation', help_text='Enter the same password as before, for verification.')
  
  def clean_password_confirm(self):
    password = self.cleaned_data['password1']
    password_confirm = self.cleaned_data.get('password2')
    if password and password_confirm:
        if password != password_confirm:
            raise forms.ValidationError("")
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2']

class ChangePassword(forms.Form):
  def clean(self):
    data = self.cleaned_data
    password1 = data['password1']
    password2 = data['password2']

    
    if password1 != password2:
      raise forms.ValidationError("Passwords do not match.")
  
  old_password = forms.CharField(widget = forms.PasswordInput, label = 'Old Password')
  password1 = forms.CharField(widget = forms.PasswordInput, label = 'New Password')
  password2 = forms.CharField(widget = forms.PasswordInput, label = 'New Password Confirmation', help_text='Enter the same password as before, for verification.<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>')
  password = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class EditTurtleCreateFormArchived(forms.Form):
  def clean(self):
    data = self.cleaned_data
    r_num = data['r_num']
    hatchling_num = data['hatchling_num']
    year_archived = data['year_archived']

    if Turtle.objects.filter(valid_to = None, r_num = r_num, hatchling_num = hatchling_num, year_archived = year_archived).exists():
      raise forms.ValidationError('This turtle already exists.')

  r_num = forms.IntegerField(label = 'R Number')
  hatchling_num = forms.IntegerField(label = 'Hatchling Number')
  archived = forms.BooleanField(required=False, label = 'Archived', widget=forms.CheckboxInput(attrs={'checked': ''}))
  year_archived = forms.IntegerField(widget = forms.HiddenInput())

class EditTurtleCreateForm(forms.Form):
  def clean(self):
    data = self.cleaned_data
    r_num = data['r_num']
    hatchling_num = data['hatchling_num']
    year_archived = data['year_archived']

    if Turtle.objects.filter(valid_to = None, r_num = r_num, hatchling_num = hatchling_num, year_archived = year_archived).exists():
      raise forms.ValidationError('This turtle already exists.')

  r_num = forms.IntegerField(label = 'R Number')
  hatchling_num = forms.IntegerField(label = 'Hatchling Number')
  archived = forms.BooleanField(required=False, label = 'Archived')
  year_archived = forms.IntegerField(widget = forms.HiddenInput())

class NewTurtleCreateForm(forms.ModelForm):
  def clean(self):
    data = self.cleaned_data
    r_num = data['r_num']
    hatchling_num = data['hatchling_num']

    if Turtle.objects.filter(archived = False, r_num = r_num, hatchling_num = hatchling_num, valid_to = None).exists():
      raise forms.ValidationError("This turtle already exists.")
    
    return data
  
  editor = forms.CharField(widget=forms.HiddenInput)

  class Meta:
    model = Turtle
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
  
  def __init__(self, *args, **kwargs):
    super(NewMeasurementCreateForm, self).__init__(*args, **kwargs)
    self.fields['turtle'].queryset = Turtle.objects.all().filter(valid_to=None, archived=False)
  
  class Meta:
    model = Measurement
    fields = ['turtle','date', 'carapace_length', 'carapace_width', 'carapace_height', 'plastron_length', 'mass', 'editor']

class NewContactForm(forms.Form):
  email = forms.EmailField(label = 'Your Email')
  subject = forms.CharField(label = 'Subject')
  body = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label='Body')

class NewSearchForm(forms.Form):  
  def clean(self):
    data = self.cleaned_data
    archived = data['archived']
    year_archived = data['year_archived']

    if archived and not year_archived:
      raise forms.ValidationError("Please enter a year archived when searching for archived turtles.")
  
  r_num = forms.IntegerField(label = 'R Number')
  archived = forms.BooleanField(required=False, label = 'Archived?')
  year_archived = forms.IntegerField(required=False, label = 'Year Archived')

class UserConfirmationForm(forms.Form):
  code = forms.IntegerField(label='Confirmation Code', validators=[MaxValueValidator(99999), MinValueValidator(10000)])

class NewDeleteForm(forms.Form):
  confirmation = forms.CharField(label = 'Type the letters above to confirm account deletion')
  delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class ForgotForm(forms.Form):
  email = forms.EmailField(label = 'Email', help_text='Please use your ocvts.org email.')

  def clean(self):
    data = self.cleaned_data
    email = data['email']

    if not User.objects.filter(email = email, is_active = True).exists():
      raise forms.ValidationError("This user does not exist.")

class ChangeNameForm(forms.Form):
  first_name = forms.CharField(label = 'First Name')
  last_name = forms.CharField(label = 'Last Name')
  name = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class LoginForm(forms.Form):
  def clean(self):
    data = self.cleaned_data
    username = data['username']

    if User.objects.filter(username = username).exists() == False:
      raise forms.ValidationError("Please enter a correct username.")
  
  username = forms.CharField(label='Username')
  password = forms.CharField(label='Password', widget = forms.PasswordInput)