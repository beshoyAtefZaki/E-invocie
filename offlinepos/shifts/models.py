from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from posprofile.models import PosProfile
# Create your models here.
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver

class OpenEntey(models.Model):
    posprofile = models.ForeignKey(PosProfile , on_delete= CASCADE)
    opentime = models.DateTimeField( auto_now_add=True)
    cash = models.DecimalField(decimal_places=3 , max_digits=10 ,default=0)
    credit = models.DecimalField(decimal_places=3 , max_digits=10,default=0)
    docstatus = models.CharField(max_length=20 , default="Open" )
    invoices= models.IntegerField(default=0, null=True,blank=True)
    closing_cash = models.DecimalField(decimal_places=3 , max_digits=10,default=0)
    closing_credit = models.DecimalField(decimal_places=3 , max_digits=10,default=0)
    close_at = models.DateTimeField(auto_now= False , null= True ,blank=True)
    remote_name  = models.CharField(max_length= 250 , null =True , blank=True)
    synced = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id ) + str(self.docstatus)  +str(self.opentime)


class CloseEntry(models.Model):
    open_entry = models.ForeignKey(OpenEntey , on_delete=CASCADE)
    closing_time = models.DateTimeField( auto_now_add=True)
    cash = models.DecimalField(decimal_places=3 , max_digits=10 ,default=0)
    credit = models.DecimalField(decimal_places=3 , max_digits=10,default=0)
    docstatus = models.CharField(max_length=20 , default="Open" )
    invoices= models.IntegerField(default=0, null=True,blank=True)
    closing_cash = models.DecimalField(decimal_places=3 , max_digits=10,default=0)
    closing_credit = models.DecimalField(decimal_places=3 , max_digits=10,default=0)
    remote_name  = models.CharField(max_length= 250 , null =True , blank=True)
    synced = models.BooleanField(default=False)



@receiver(pre_save, sender=OpenEntey)
def create_close_entry(sender , instance , **kwargs) :
    if instance.docstatus =="Close" :
        n_close = CloseEntry(
            open_entry = instance ,
            closing_time = datetime.now() , 
            cash = instance.closing_cash ,
            credit = instance.closing_credit,
        )
        n_close.save()
    else:
        pass