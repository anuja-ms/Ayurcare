from django.db import models

class tbl_district(models.Model):
    district_id=models.AutoField(primary_key=True)
    district_name=models.CharField(max_length=25)

class tbl_location(models.Model):
    location_id=models.AutoField(primary_key=True)
    location_name=models.CharField(max_length=25) 
    district_id=models.ForeignKey(tbl_district,on_delete=models.CASCADE)   
    

# Create your models here.
