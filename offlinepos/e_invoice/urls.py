from django.contrib import admin
from django.urls import path , include
from.serializers import e_invoice_form

from .views import   invoice_list
urlpatterns = [
    path('create' ,e_invoice_form , name='create' ),
    path('list' ,invoice_list , name='list-einvoice' )
      
]
