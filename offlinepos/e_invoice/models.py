from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import pre_save ,post_save
from django.db.models import Sum
from django.dispatch import receiver
# Create your models here.



class TaxTotals (models.Model):
    taxType = models.CharField(max_length=250 )
    amount = models.DecimalField(decimal_places=5 ,max_digits=12 )



    def __str__(self):
        return self.taxType
class  Payment(models.Model):
    bankName        = models.CharField(max_length=250 )
    bankAddress     = models.CharField(max_length= 250 , null= True , blank=True)
    bankAccountNo   = models.CharField(max_length= 250 , null= True , blank=True)
    bankAccountIBAN = models.CharField(max_length= 250 , null= True , blank=True)
    swiftCode       = models.CharField(max_length= 250 , null= True , blank=True)
    terms           =  models.CharField(max_length= 250 , null= True , blank=True)

    def __str__(self):
        return self.bankName
class taxableItems(models.Model):
    taxType = models.CharField(max_length= 250)
    amount = models.DecimalField(decimal_places= 5 , max_digits=10 , null=True , blank=True)
    subType =  models.CharField(max_length= 250)
    rate = models.DecimalField(decimal_places= 5 , max_digits=10 ,null=True ,blank=True)

class InvoiceLine(models.Model):
    description = models.CharField(max_length=250)
    itemType = models.CharField(max_length=250)
    itemCode =  models.CharField(max_length=250)
    unitType = models.CharField(max_length=250)
    quantity = models.DecimalField(decimal_places=2 , max_digits=10)
    unitValue_currencySold =  models.CharField(max_length=250, default='EGP')
    unitValue_amountEGP = models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True)
    unitValue_amountSold = models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True)
    unitValue_currencyExchangeRate =  models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True)
    salesTotal = models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True)
    total = models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True)
    valueDifference =models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True , default=0) 
    totalTaxableFees = models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True , default=0)
    netTotal = models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True , default=0)
    itemsDiscount =  models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True , default=0)
    discount_rate =models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True , default=0)
    discount_amount=models.DecimalField(decimal_places=5 , max_digits=12 ,null=True , blank=True , default=0)
    taxableItems = models.ManyToManyField(taxableItems , null=True , blank=True) 
    internalCode =  models.CharField(max_length=250 , null=True , blank=True)



def round_f(value):
    return (round(value , 5) )

@receiver(pre_save, sender=InvoiceLine)
def caculateTotlas(sender , instance, **kwargs ):
    try:
        item_discount = round((float(instance.discount_amount or 0) / float(instance.quantity)) ,5)
        instance.salesTotal =round(( float(instance.quantity or 0 ) *float(instance.unitValue_amountEGP or 0)),5)
        instance.netTotal = round ((((float(instance.unitValue_amountEGP or 0) -float(item_discount or 0) )*float(instance.quantity or 0)) ),5)
        #caculate total taxes
        total_taxes = 0 
        taxes = instance.taxableItems.all()
        for tax in taxes :
            total_taxes +=  float(tax.amount or 0 )
        instance.total = round((float(total_taxes or 0) + float(instance.netTotal or 0 )),5)
    except:pass






class EInvoice (models.Model) :
    #issuer info
    issuer_type =models.CharField(max_length=250)
    issuer_id=models.CharField(max_length=250)
    issuer_name=models.CharField(max_length=250)
    issuer_address_branchId=models.CharField(max_length=250)
    issuer_address_country=models.CharField(max_length=250)
    issuer_address_governate=models.CharField(max_length=250)
    issuer_address_regionCity=models.CharField(max_length=250)
    issuer_address_street=models.CharField(max_length=250)
    issuer_address_buildingNumber=models.CharField(max_length=250)
    #receiver Info
    receiver_type =models.CharField(max_length=250)
    receiver_id=models.CharField(max_length=250)
    receiver_name=models.CharField(max_length=250)
    receiver_address_branchId=models.CharField(max_length=250)
    receiver_address_country=models.CharField(max_length=250)
    receiver_address_governate=models.CharField(max_length=250)
    receiver_address_regionCity=models.CharField(max_length=250)
    receiver_address_street=models.CharField(max_length=250)
    receiver_address_buildingNumber=models.CharField(max_length=250)
    documentType = models.CharField(max_length= 250)
    documentTypeVersion =  models.CharField(max_length= 250)
    dateTimeIssued = models.DateTimeField(auto_now= False ,auto_now_add=False ,blank=True ,null=True)
    taxpayerActivityCode = models.CharField(max_length= 250)
    internalId= models.CharField(max_length= 250)
    purchaseOrderReference = models.CharField(max_length= 250 , null=True , blank=True)
    purchaseOrderDescription = models.CharField(max_length= 250 , null=True , blank=True)
    salesOrderReference = models.CharField(max_length= 250 , null=True , blank=True)
    salesOrderDescription =  models.CharField(max_length= 250 , null=True , blank=True)
    proformaInvoiceNumber = models.CharField(max_length= 50 , null=True , blank=True)
    payment = models.ForeignKey(Payment , on_delete=CASCADE , null=True , blank=True)
    invoiceLines = models.ManyToManyField(InvoiceLine)
    totalSalesAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True , blank=True)
    totalDiscountAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True , blank=True)
    netAmount = models.DecimalField(max_digits=10 , decimal_places=5 ,null=True , blank=True)
    taxTotals = models.ManyToManyField(TaxTotals ,null=True , blank=True)
    extraDiscountAmount =  models.DecimalField(max_digits=100 , decimal_places=5 ,null=True,blank=True)
    totalItemsDiscountAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True,blank=True)
    totalAmount = models.DecimalField(max_digits=10 , decimal_places=5 ,null=True,blank=True)
    submissionId =models.CharField(max_length=500 , blank=True , null=True)
    docstatus =models.CharField(max_length=500 , blank=True , null=True)
    errro_log =models.CharField(max_length=500 , blank=True , null=True)

@receiver(pre_save ,sender=EInvoice)
def invoice_totals(sender ,instance , **kwargs):
    try:
        totalSalesAmount = 0
        totalDiscountAmount = 0
        tax_totals={}
        
        for line in instance.invoiceLines.all():
            order_line = InvoiceLine.objects.get(id=line.id)
            order_line.save()
            for tax_type in order_line.taxableItems.all():
            
                    tax_found = False
                    for key in tax_totals.keys():
                        if key == tax_type.taxType :
                            val = float(tax_totals.get(key)) + float(tax_type.amount)
                            tax_totals[key] = val
                            tax_found = True
                        # else :
                        #     tax_totals[tax_type.taxType] =float(tax_type.amount)
                    # else :
                    if not tax_found :
                        tax_totals[tax_type.taxType] =float(tax_type.amount)

            totalSalesAmount += line.salesTotal
            totalDiscountAmount += line.discount_amount

    
        for tax_type_name , tax_type_amount  in tax_totals.items():
            instance.taxTotals.create(taxType = tax_type_name , amount = tax_type_amount)
        instance.totalDiscountAmount =  round(float(totalDiscountAmount or 0 ) , 5 )
        instance.totalSalesAmount = round(float(totalSalesAmount) , 5)
        # instance.netAmount = totalSalesAmount -totalDiscountAmount 
        instance.totalAmount = 0.0
    except:pass


class EInovie_settinge(models.Model):
    tax_id = models.CharField(max_length= 250)
    user_token = models.CharField(max_length= 250)
    user_key = models.CharField(max_length= 250)
    token_key = models.CharField(max_length=500 , null=True , blank=True)
    issuer_type =models.CharField(max_length=250 , null=True , blank=True)
    issuer_id=models.CharField(max_length=250, null=True , blank=True)
    issuer_name=models.CharField(max_length=250, null=True , blank=True)
    issuer_address_branchId=models.CharField(max_length=250, null=True , blank=True )
    issuer_address_country=models.CharField(max_length=250, null=True , blank=True)
    issuer_address_governate=models.CharField(max_length=250, null=True , blank=True)
    issuer_address_regionCity=models.CharField(max_length=250, null=True , blank=True)
    issuer_address_street=models.CharField(max_length=250, null=True , blank=True)
    issuer_address_buildingNumber=models.CharField(max_length=250, null=True , blank=True)



 
