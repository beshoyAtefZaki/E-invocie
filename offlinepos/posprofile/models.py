from django.db import models
# from item.models import ItemGroup
# Create your models here.

class Tax (models.Model):
    rate = models.CharField(max_length=10  )


class PaymentMethod(models.Model):
    name=  models.CharField(max_length= 200)

class PosProfile (models.Model) :
    name= models.CharField(max_length=200 )
    server_url = models.CharField(max_length=250 , null=True , blank=True)
    appkey = models.CharField(max_length=200 )
    appsecret = models.CharField(max_length=200)
    pricelist = models.CharField(max_length=200)
    itemgroup = models.CharField(max_length=200 , null=True , blank=True)
    taxes = models.ManyToManyField(Tax)
    pymanet_method = models.ManyToManyField(PaymentMethod)



    def __str__(self) :
        return self.name
    