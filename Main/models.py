from django.db import models
from django.db import models
# Create your models here.

'''
    - HospitalInfo : LL's of Hospital with email 
    - CCTVIds      : LL's of CCTV 
'''




class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    mob = models.CharField(max_length=15)
    msg = models.TextField()

    def __str__(self):
        return f"{self.fname} {self.lname} {self.msg}"


class Route(models.Model):
    start = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f" Start : {self.start} End : {self.destination}"

