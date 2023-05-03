from django import forms
from .models import Turtle, Measurement

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