from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class singlestock(models.Model):
    name = models.CharField(max_length=20)
    sector = models.CharField(max_length=20)
    cap = models.CharField(max_length=20)
    last_trade_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    yearly = models.FloatField()
    q1 = models.FloatField()
    q2 = models.FloatField()
    q3 = models.FloatField()
    hold = models.BooleanField(default=False)

    def __str__(self):
        return self.name +" - " +self.sector

class profile(models.Model):
    name = models.CharField(max_length=100)
    photo = models.FileField()
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    company = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    stocks = models.ManyToManyField(singlestock)

    def __str__(self):
        return self.name + " " +self.company + " "+ str(self.age)

class feedback(models.Model):
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)


    def __str__(self):
        return self.name