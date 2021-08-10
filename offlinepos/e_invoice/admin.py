from django.contrib import admin

# Register your models here.
from .models import taxableItems,InvoiceLine,EInvoice, EInovie_settinge

admin.site.register(taxableItems)
admin.site.register(InvoiceLine)
admin.site.register(EInvoice)
admin.site.register(EInovie_settinge)

