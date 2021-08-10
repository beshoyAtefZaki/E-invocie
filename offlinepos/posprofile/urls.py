

from django.urls import path
from .views import *
urlpatterns = [
    path('', home , name='home'),
    path('profile', pos_profile , name='profile'),
    path('orders/<id>' , orders , name='orders'),
    path('order/<id>' ,order_details , name="order_details"),
     path('order_detail/<id>' ,edit_order , name="edit_order") ,
     path('remove' , remove_item , name ='remove') ,
     path('delete/<id>' , delete_order , name="delete"),
     path('submit/<id>' , submit_order , name="submit")
]
