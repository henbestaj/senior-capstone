from django.db import models
from django.utils import timezone

# Create your models here.
class Turtle(models.Model):
  r_num = models.IntegerField(verbose_name = "R Number")
  hatchling_num = models.IntegerField(verbose_name = "Hatchling Number")
  editor = models.TextField(default = "Administrator", verbose_name = "Editor")
  archived = models.BooleanField(default = False)
  valid_from = models.DateTimeField(default = timezone.now, verbose_name = "Valid From")
  valid_to = models.DateTimeField(null = True, blank = True, verbose_name = "Valid To")
  previous_turtle = models.ForeignKey('self', null = True, blank = True, default = None, on_delete = models.CASCADE, verbose_name = "Previous Turtle")
  def get_absolute_url(self):
    return "/current/"
  def __str__(self):
    return self.r_num + "-" + self.hatchling_num

class Measurement(models.Model):
  date = models.DateField(default = timezone.now, verbose_name = "Date")
  carapace_length = models.FloatField(null = True, blank = True, verbose_name = "Carapace Length")
  carapace_width = models.FloatField(null = True, blank = True, verbose_name = "Carapace Width")
  plastron_length = models.FloatField(null = True, blank = True, verbose_name = "Plastron Length")
  carapace_height = models.FloatField(null = True, blank = True, verbose_name = "Carapace Height")
  mass = models.FloatField(null = True, blank = True, verbose_name = "Mass")
  turtle = models.ForeignKey(Turtle, null = True, blank = True, on_delete = models.CASCADE, verbose_name = "Turtle")
  editor = models.TextField(default = "Administrator", verbose_name = "Editor")
  valid_from = models.DateTimeField(default = timezone.now, verbose_name = "Valid From")
  valid_to = models.DateTimeField(null = True, blank = True, verbose_name = "Valid To")
  previous_measurment = models.ForeignKey('self', null = True, blank = True, default = None, on_delete = models.CASCADE, verbose_name = "Previous Measurment")

  def get_absolute_url(self):
    return "/current/"
  
  def __str__(self):
    return self.turtle.r_num + "-" + self.turtle.hatchling_num + ": " + self.date
