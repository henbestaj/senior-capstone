from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class Turtle(models.Model):
  r_num = models.PositiveIntegerField(verbose_name = "R Number")
  hatchling_num = models.PositiveIntegerField(verbose_name = "Hatchling Number")
  editor = models.TextField(default = "Administrator", verbose_name = "Editor")
  archived = models.BooleanField(default = False, verbose_name = "Archived")
  year_archived = models.PositiveIntegerField(default = 0, verbose_name = "Year Archived")
  valid_from = models.DateTimeField(default = timezone.now, verbose_name = "Valid From")
  valid_to = models.DateTimeField(null = True, blank = True, verbose_name = "Valid To")
  previous_turtle = models.ForeignKey('self', null = True, blank = True, default = None, on_delete = models.CASCADE, verbose_name = "Previous Turtle")

  def get_absolute_url(self):
    return "/current/"
  
  def __str__(self):
    if self.archived:
      return str(self.r_num) + "-" + str(self.hatchling_num) + " (archived " + str(self.year_archived) + ")"
    else:
      return str(self.r_num) + "-" + str(self.hatchling_num) + " (active)"

class Measurement(models.Model):
  date = models.DateField(default = timezone.now, verbose_name = "Date")
  carapace_length = models.FloatField(null = True, blank = True, verbose_name = "Carapace Length", validators=[MinValueValidator(0)])
  carapace_width = models.FloatField(null = True, blank = True, verbose_name = "Carapace Width", validators=[MinValueValidator(0)])
  plastron_length = models.FloatField(null = True, blank = True, verbose_name = "Plastron Length", validators=[MinValueValidator(0)])
  carapace_height = models.FloatField(null = True, blank = True, verbose_name = "Carapace Height", validators=[MinValueValidator(0)])
  mass = models.FloatField(null = True, blank = True, verbose_name = "Mass", validators=[MinValueValidator(0)])
  turtle = models.ForeignKey(Turtle, on_delete = models.CASCADE, verbose_name = "Turtle")
  editor = models.TextField(default = "Administrator", verbose_name = "Editor")
  valid_from = models.DateTimeField(default = timezone.now, verbose_name = "Valid From")
  valid_to = models.DateTimeField(null = True, blank = True, verbose_name = "Valid To")
  previous_measurment = models.ForeignKey('self', null = True, blank = True, default = None, on_delete = models.CASCADE, verbose_name = "Previous Measurment")

  def get_absolute_url(self):
    return "/current/"

  @property
  def display_turtle(self):
    return str(self.turtle.r_num) + "-" + str(self.turtle.hatchling_num)

  def __str__(self):
    return str(self.turtle.r_num) + "-" + str(self.turtle.hatchling_num) + ": " + str(self.date)
