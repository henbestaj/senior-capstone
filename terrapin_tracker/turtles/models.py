from django.db import models
import datetime

# Create your models here.
class Turtle(models.Model):
  r_num = models.IntegerField()
  hatchling_num = models.IntegerField()
  def __str__(self):
    return self.r_num + '-' + self.hatchling_num

class Measurement(models.Model):
  date = models.DateField(default = datetime.date.today())
  carapace_length = models.FloatField()
  carapace_width = models.FloatField()
  plastron_length = models.FloatField()
  carapace_height = models.FloatField()
  mass = models.FloatField()
  turtle = models.ForeignKey(Turtle, on_delete = models.CASCADE)
  def __str__(self):
    return self.turtle.r_num + '-' + self.turtle.hatchling_num + ': ' + self.date