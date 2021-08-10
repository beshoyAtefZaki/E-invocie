from rest_framework import serializers
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.http import require_http_methods
import os
from .models import *

# @api_view(['POST','GET'])
# @require_http_methods(["GET", "POST"])
@api_view(['POST','GET'])
def e_invoice_form(request):
    if request.method == "GET":
        return JsonResponse({"home":"home"})
    if request.method=="POST" :
        # print(request.data.get('documents'))
        for invoice in request.data.get('documents'):
            try :
                os.remove('/home/beshoy/production/qbexpress/sFile.txt')
            except:pass
            file = open('/home/beshoy/production/qbexpress/sFile.txt' , 'a' )
            file.write(json.dumps(invoice) )
            #EInovie_settinge
            ic_invoice = EInvoice()
            #set issuer data need to update to set default issuer data
            issuer                                   = invoice.get('issuer')

            ic_invoice.issuer_type                   = issuer.get('type')
            ic_invoice.issuer_id                     = issuer.get('id')
            ic_invoice.issuer_name                   = issuer.get('name')
            address                                  = issuer.get('address')
            ic_invoice.issuer_address_branchId       = address.get('branchID')
            ic_invoice.issuer_address_country        = address.get('country')
            ic_invoice.issuer_address_governate      = address.get('governate')
            ic_invoice.issuer_address_regionCity     = address.get('regionCity')
            ic_invoice.issuer_address_street         = address.get('street')
            ic_invoice.issuer_address_buildingNumber = address.get('buildingNumber')

            #set recevier data
            receiver = invoice.get('receiver')
            ic_invoice.receiver_type                   = receiver.get('type')
            ic_invoice.receiver_id                     = receiver.get('id')
            ic_invoice.receiver_name                   = receiver.get('name')
            receiver_address                           = receiver.get('address')
            ic_invoice.receiver_address_branchId       = receiver_address.get('branchID')
            ic_invoice.receiver_address_country        = receiver_address.get('country')
            ic_invoice.receiver_address_governate      = receiver_address.get('governate')
            ic_invoice.receiver_address_regionCity     = receiver_address.get('regionCity')
            ic_invoice.receiver_address_street         = receiver_address.get('street')
            ic_invoice.receiver_address_buildingNumber = receiver_address.get('buildingNumber')
              

            # set document info 
            ic_invoice.documentType = invoice.get('documentType')
            ic_invoice.documentTypeVersion= invoice.get('documentTypeVersion')
            ic_invoice.dateTimeIssued = invoice.get('dateTimeIssued')
            
            ic_invoice.taxpayerActivityCode = invoice.get('taxpayerActivityCode')
            ic_invoice.internalId = invoice.get('internalID')
            ic_invoice.save()
            #set Invoice Items 
            invoiceLines = invoice.get('invoiceLines')
            
            for line in invoiceLines :
                taxes = line.get('taxableItems')
                # taxes_list = [{tax.}]
                unitValue = line.get('unitValue')
                ic_invoice.invoiceLines.create(
                       description = line.get('description'),
                        itemType = line.get('itemType'),
                        itemCode = line.get('itemCode'),
                        unitType = line.get('unitType') ,
                        quantity = line.get('quantity'),
                        unitValue_currencySold = unitValue.get('currencySold'),
                        unitValue_amountEGP  = unitValue.get('amountEGP') ,


                        



                )
            
            # ic_invoice.save()


        return JsonResponse({"creates":"created"})