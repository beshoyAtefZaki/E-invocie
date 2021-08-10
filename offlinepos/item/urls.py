
from django.urls import path
from .views import *
urlpatterns = [
   path('' ,item_list , name= "item_list" )
]
