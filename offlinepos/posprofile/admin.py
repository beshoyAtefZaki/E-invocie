from django.contrib import admin
from .models import PosProfile , PaymentMethod
# Register your models here.
admin.site.register(PosProfile)
admin.site.register(PaymentMethod)