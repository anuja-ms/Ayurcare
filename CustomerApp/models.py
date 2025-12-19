from django.db import models
from GuestApp.models import tbl_customer
from HospitalApp.models import tbl_package

# Create your models here.
class tbl_booking(models.Model):
    booking_id=models.AutoField(primary_key=True)
    package_id=models.ForeignKey(tbl_package,on_delete=models.CASCADE) 
    customer_id=models.ForeignKey(tbl_customer,on_delete=models.CASCADE) 
    status=models.CharField(max_length=100)
    booking_date=models.DateField(auto_now_add=True)
    require_date=models.DateField()
    t_amount=models.IntegerField()
    reason=models.CharField(max_length=100)
    
class tbl_payment(models.Model):
    payment_id=models.AutoField(primary_key=True)
    booking_id=models.ForeignKey(tbl_booking,on_delete=models.CASCADE) 
    status=models.CharField(max_length=100)
    payment_date=models.DateField(auto_now_add=True)
    commission=models.IntegerField(null=True)


class tbl_feedback(models.Model):
    feedback_id=models.AutoField(primary_key=True)
    package_id=models.ForeignKey(tbl_package,on_delete=models.CASCADE) 
    rating=models.IntegerField()
    feedback=models.CharField(max_length=500)
    customer_id=models.ForeignKey(tbl_customer,on_delete=models.CASCADE) 
    date=models.DateField(auto_now_add=True)