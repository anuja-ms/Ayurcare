from django.db import models
from AdminApp.models import tbl_location

# Create your models here.
class tbl_login(models.Model):
    login_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=25)
    password=models.CharField(max_length=25)
    role=models.CharField(max_length=25)
    status=models.CharField(max_length=25,default='')

class tbl_hospital(models.Model):
    hospital_id=models.AutoField(primary_key=True)
    hospital_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    address=models.CharField(max_length=100)
    image=models.ImageField()
    idproof=models.ImageField()
    location_id=models.ForeignKey(tbl_location,on_delete=models.CASCADE)
    login_id=models.ForeignKey(tbl_login,on_delete=models.CASCADE)

class tbl_customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    address=models.CharField(max_length=100)
    image=models.ImageField()
    idproof=models.ImageField()
    location_id=models.ForeignKey(tbl_location,on_delete=models.CASCADE)
    login_id=models.ForeignKey(tbl_login,on_delete=models.CASCADE)
    
