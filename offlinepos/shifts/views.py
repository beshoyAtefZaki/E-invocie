
from django.db import connection
from django.shortcuts import redirect, render
from item.models import ItemGroup, Order ,RemoteInitItem
from posprofile.models import PosProfile ,PaymentMethod , Tax
from .models import OpenEntey ,CloseEntry 
from datetime import datetime
# Create your views here.
from item.get_server_item import get_remote_item
from posprofile.server_data import create_open_entry as remote_entry  , check_connection ,get_pos_info
from posprofile.views import create_remote_pos
from django.db.models import Q
from item.models import Item , ItemGroup


def create_open_entry(pos_profile):
    connection = check_connection(pos_profile.appkey , pos_profile.appsecret ,pos_profile.server_url)
    if connection :
        status = connection
    else :
        status = 'Of Line'

    
    
    
   
    
    entry = OpenEntey()
    if status != 'Of Line' :
        url  = str(pos_profile.server_url)
        pos_name = pos_profile.name
        remote= remote_entry(url , pos_profile.appkey , pos_profile.appsecret, pos_name)
        entry.remote_name = remote
        entry.synced = True
    entry.posprofile = pos_profile


    entry.save()
    return 1


def create_close_entry(openEntryid):
    openentry = OpenEntey.objects.get(id =openEntryid)
    openentry.docstatus ="Close" 
    openentry.save()
    return 1




def home(request) :
    temp = "open.html"
    open_orders =0
    invoices = 0
    profile = PosProfile.objects.filter(id =1).first()
    remote__init, created = RemoteInitItem.objects.get_or_create(
        id = 1,
    )
    if profile :
        pos = get_pos_info(profile.server_url , profile.appkey , profile.appsecret,profile.name )
        ex_group = ItemGroup.objects.all()
        if pos :
            print(pos)
            if len(pos.get('item_groups' )) > 0:
                Item.objects.filter(~Q(item_group__in =pos.get('item_groups' ))).delete()
                ItemGroup.objects.filter(~Q(name__in =pos.get('item_groups' ))).delete()
            payment_method = profile.pymanet_method.all()
            methods = profile.pymanet_method.all()
            for per in pos.get('payment_methods') :
                if per not in [n.name for n in payment_method] and pos :
                    a,c = PaymentMethod.objects.get_or_create(name = per)
                    a.save()
                    profile.pymanet_method.add(PaymentMethod.objects.get(name = per))
            if len (pos.get('taxes')) > 0 :
                tax_rate = pos.get('taxes')
                Tax.objects.filter(~Q(rate__in = [tax.get('rate') for tax in tax_rate ])).delete()
                taxes = profile.taxes.all()
                for tax in pos.get('taxes'):
                    if tax.get('rate')  not in [n.rate for n in taxes] :
                        a,c = Tax.objects.get_or_create(rate = tax.get('rate'))
                        a.save()
                        profile.taxes.add(a)
                        


            a , f = Tax.objects.get_or_create(rate = 0)
            profile.save()

       

    if not remote__init.inited and profile :
        get_remote_item(profile.server_url , profile.appkey , profile.appsecret, profile.name , True) 
        if get_remote_item :
            remote__init.inited = True
            remote__init.save()
    else :
         get_remote_item(profile.server_url , profile.appkey , profile.appsecret, profile.name , False)

    orders = Order.objects.filter(orderstatus = "Open")
    openEntry = OpenEntey.objects.filter(posprofile = profile , docstatus= "Open").first()
   
    try :
        create_sync_unsynced()
    except:
        pass
    if openEntry :
         open_orders = Order.objects.filter(orderstatus = "Open" , open_entry = openEntry).count()
         invoices= Order.objects.filter(orderstatus = "Submited" , open_entry = openEntry).count()

    content =   {"active": "nav-link active"  ,
                "deactive" : "nill",
                "active_session" : openEntry if openEntry else None,
                "profile" : profile.name if profile else None ,
                "open_orders" : open_orders,
                "invoices" :invoices
                }
    

    content["orders"] = orders
    if request.method =="POST" and not openEntry and profile:
        a = create_open_entry(profile)
        return redirect('main')
   
    return render(request , temp, content )


def close_view(request) :
    if request.method=='POST' :
        EntryId = request.POST.get("EntryId")
        if EntryId :
            create_close_entry(EntryId)
        return redirect('main')
    else:
        return redirect('main')



#shift Orders List 

def order_list (request) :
    open_entry = OpenEntey.objects.filter(docstatus="Open").first()
    orders =  Order.objects.filter(orderstatus = "Open")
    if open_entry :
        orders =  Order.objects.filter(orderstatus = "Open" , open_entry =open_entry)
    content = {
        "orders" : orders ,
        "open_entry" : open_entry,
        "active_session":open_entry
    }
    return render (request , 'order_list.html' , content)


def invoice_list (request) :
    open_entry = OpenEntey.objects.filter(docstatus="Open").first()
    orders =  Order.objects.filter(orderstatus = "Submited")
    if open_entry :
        orders =  Order.objects.filter(orderstatus = "Submited" , open_entry =open_entry)
    content = {
        "orders" : orders ,
        "open_entry" : open_entry,
        "active_session":open_entry
    }
    return render (request , 'order_list.html' , content)



def create_sync_unsynced():
    profile = PosProfile.objects.filter(id =1).first()
    open_entry = OpenEntey.objects.filter(docstatus="Open").first()
    if profile and open_entry :
        connection = check_connection(profile.appkey , profile.appsecret ,profile.server_url)
        if connection:
            if open_entry.synced == False:
                remote= remote_entry(profile.server_url , profile.appkey , profile.appsecret, profile.name)
                open_entry.remote_name = remote
            
                open_entry.synced = True
                open_entry.save()
            orders = Order.objects.filter(open_entry = open_entry , synced=False , orderstatus='Submited')
            for i in orders :
                if i.synced == False :
                    r = create_remote_pos(i.id)
                    print(r)
                    i.synced = True
                    i.save()

            

            
    