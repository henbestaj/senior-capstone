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

class NewMeasurmentCreateForm(forms.ModelForm):
  class Meta:
    model = Measurement
    fields = '__all__'

class EditMeasurmentCreateForm(forms.ModelForm):
  class Meta:
    model = Measurement
    fields = '__all__'