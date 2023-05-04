from django import forms
from .models import Turtle, Measurement
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator

# Inherit Django's default UserCreationForm
class UserRegisterForm(UserCreationForm):
  def clean_email(self):
    if "@ocvts.org" not in self.cleaned_data['email'] and "@mail.ocvts.org" not in self.cleaned_data['email']:
      raise forms.ValidationError("Must be a ocvts.org email address.")
    return self.cleaned_data['email']
  
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class NewTurtleCreateForm(forms.ModelForm):
  class Meta:
    model = Turtle
    fields = ['r_num', 'hatchling_num', 'archived']

# class EditTurtleCreateForm(forms.ModelForm):
#   class Meta:
#     model = Turtle
#     fields = '__all__'

class NewMeasurementCreateForm(forms.ModelForm):
  class Meta:
    model = Measurement
    fields = ['turtle','date', 'carapace_length', 'carapace_width', 'carapace_height', 'plastron_length', 'mass']

# class EditMeasurementCreateForm(forms.ModelForm):
#   class Meta:
#     model = Measurement
#     fields = '__all__'

class NewContactForm(forms.Form):
  email = forms.EmailField(label = 'Email')
  subject = forms.CharField(label = 'Subject')
  body = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label='Body')

class NewSearchForm(forms.Form):  
  r_num = forms.IntegerField(label = 'R Number')
  archived = forms.BooleanField(required=False, label = 'Archived?')
  year_archived = forms.IntegerField(required=False, label = 'Year Archived')

class UserConfirmationForm(forms.Form):
  code = forms.IntegerField(validators=[MaxValueValidator(99999), MinValueValidator(10000)])