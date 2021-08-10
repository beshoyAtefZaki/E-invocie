from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.signals import pre_save
from django.db.models import Sum
from django.dispatch import receiver
from shifts.models import OpenEntey
# Create your models here.
from posprofile.models import PosProfile

class ItemGroup(models.Model) :
    name = models.CharField(max_length= 100 ,unique=True)

    def __str__(self):
        return self.name



class Item (models.Model) :
    item_code = models.CharField(max_length=200)
    item_name = models.CharField(max_length=200)
    item_arabic_name= models.CharField(max_length=200 , null=True , blank=True)
    stock_uom = models.CharField(max_length=200, blank=True , null=True)
    pricelist_rate= models.DecimalField(max_digits =10 ,decimal_places=2 , blank=True , null=True )
    actual_qty = models.IntegerField(default=0)
    item_group = models.CharField(max_length=200, blank=True , null=True)

    

    def __str__(self):
        return self.item_code

class RemoteInitItem(models.Model) :
    inited = models.BooleanField(default=False)
    def __str__(self):
        return str(self.inited)
class OrderLine(models.Model) :
    item = models.ForeignKey(Item,on_delete=CASCADE) 
    price = models.DecimalField(decimal_places=2 , max_digits=10 , default=0)
    qty = models.IntegerField(default=1)
    total= models.DecimalField(decimal_places=2 , max_digits=20 , default=0.0)



class Order(models.Model):
    open_entry = models.ForeignKey(OpenEntey , on_delete=CASCADE , null=True , blank=True)
    customer = models.CharField(max_length=200 , blank=True , null=True , default="Pos Customer" )
    items = models.ManyToManyField(OrderLine,blank=True,null=True )
    taxcategory = models.CharField(max_length=200 , null= True , blank=True)
    paymentmethod = models.CharField(max_length=200 ,default="Cash")
    discount = models.DecimalField(decimal_places=2 , max_digits=10 ,default=0 , null=True , blank=True)
    taxes = models.DecimalField(decimal_places=2 , max_digits=10 ,default=0.0 , blank=True , null=True) 
    # taxesamount = models.DecimalField(decimal_places=2 , max_digits=10)
    total = models.DecimalField(decimal_places=2 , max_digits=20 , default=0.0)
    grandtotal =  models.DecimalField(decimal_places=2 , max_digits=20 ,default=0.0)
    orderstatus = models.CharField(max_length=200 , null=True , blank=True)
    remote_name  = models.CharField(max_length= 250 , null =True , blank=True)
    synced = models.BooleanField(default=False)
    



@receiver(pre_save, sender=OrderLine)
def caculateTotlas(sender , instance, **kwargs ):
    instance.total = instance.qty *float(instance.price or 0)
    #caculate total order 



def caculate_taxes(total):
    profile = PosProfile.objects.filter(id=1).first()
    tax = 0 
    if profile :
        for rate in profile.taxes.all() :
            
            e = float(rate.rate)/100
            tax = float(tax) + round((float (total) * e ) , 3 )
          

    print(tax)
    return tax
@receiver(pre_save, sender=Order)
def caculate_order_total(sender , instance , **kwargs) :
    try :
        instance.total = 0 

        total = instance.items.all()

        for line in total :
            instance.total += line.total
        instance.taxes =float (caculate_taxes(instance.total))
        instance.grandtotal =( float(instance.taxes) + float(instance.total or 0)  ) - float(instance.discount or 0)
    except:
        pass

# @receiver(pre_save, sender=Item)
# def set_item_groups(sender , instance , **kwargs):
#       rob, created = ItemGroup.objects.get_or_create(
#         name = instance.item_group,
#              )

    
    

    




