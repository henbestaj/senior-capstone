from django import forms
from .models import Turtle, Measurement

class NewTurtleCreateForm(forms.ModelForm):
  class Meta:
    model = Turtle
    fields = '__all__'

class EditTurtleCreateForm(forms.ModelForm):
  class Meta:
    model = Turtle
    fields = '__all__'

class NewMeasurementCreateForm(forms.ModelForm):
  class Meta:
    model = Measurement
    fields = '__all__'

class EditMeasurementCreateForm(forms.ModelForm):
  class Meta:
    model = Measurement
    fields = '__all__'