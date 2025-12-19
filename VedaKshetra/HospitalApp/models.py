from django.db import models
from GuestApp.models import tbl_hospital

# Create your models here.
class tbl_package(models.Model):
    package_id=models.AutoField(primary_key=True)
    package_name=models.CharField(max_length=100) 
    image=models.ImageField()
    hospital_id=models.ForeignKey(tbl_hospital,on_delete=models.CASCADE) 
    noofdays=models.IntegerField()  
    
class tbl_service(models.Model):
    service_id=models.AutoField(primary_key=True)
    service_name=models.CharField(max_length=100) 
    image=models.ImageField()
    hospital_id=models.ForeignKey(tbl_hospital,on_delete=models.CASCADE) 
    amount=models.IntegerField() 
    description=models.CharField(max_length=100,default='') 

class tbl_packageservice(models.Model):
    ps_id=models.AutoField(primary_key=True)
    package_id=models.ForeignKey(tbl_package,on_delete=models.CASCADE) 
    service_id=models.ForeignKey(tbl_service,on_delete=models.CASCADE) 
    