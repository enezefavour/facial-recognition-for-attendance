from django.db import models



class People(models.Model):
    name = models.TextField(null=True,max_length=100)
    gender = models.TextField(null=True, max_length=20)
    image_path = models.TextField(null=True, max_length=200)
    hashed_face = models.TextField(null=True, max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    person = models.ForeignKey(People, default=1, on_delete=models.SET_DEFAULT)
    time_in = models.DateTimeField(null=True)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)
    review = models.TextField(blank=True, null=True)

