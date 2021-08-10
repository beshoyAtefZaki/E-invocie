from django.contrib import admin
from django.urls import path , include
from.serializers import e_invoice_form


urlpatterns = [
    path('create' ,e_invoice_form , name='create' )
      
]
