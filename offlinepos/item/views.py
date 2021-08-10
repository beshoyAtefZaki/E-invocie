from django.shortcuts import render ,redirect
from .models import Item ,RemoteInitItem
from posprofile.models import  PosProfile 
# Create your views here.
from .get_server_item import get_remote_item

def item_list(request) :
    profile = PosProfile.objects.filter(id=1).first()
    if not profile.name :
        return redirect('home')
    remote__init, created = RemoteInitItem.objects.get_or_create(
        id = 1,
             )
    # if created :
    #     print("created")
    # else :
    if not remote__init.inited and profile :
        get_remote_item(profile.server_url , profile.appkey , profile.appsecret, profile.name , True) 
        if get_remote_item :
            remote__init.inited = True
            remote__init.save()
    else :
         get_remote_item(profile.server_url , profile.appkey , profile.appsecret, profile.name , False)
    items = Item.objects.all()
    content  = {"items" : items ,
                "profile":profile.name}
    return render(request , "items.html" ,content)