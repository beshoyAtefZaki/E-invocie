from django.contrib import admin
from django.urls import path , include
from .views import * 
urlpatterns = [
   path('' , home, name ="main"),
   path('close' , close_view , name='close'),
   path('order_list' , order_list , name='order-list'),
    path('invoice_list' , invoice_list , name='invocie-list')



]