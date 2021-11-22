from django.db import models
from datetime import date
# Create your models here.
class URL(models.Model):
    long_url = models.CharField(max_length=100,unique=True)
    short_url = models.CharField(max_length=20,unique=True)
    clicks = models.IntegerField(default=0)
    date_created =  models.DateField(default=date.today)
    flag=models.IntegerField()


