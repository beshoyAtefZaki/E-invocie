from shifts.models import OpenEntey
from django.shortcuts import render ,redirect ,get_object_or_404
from item.models import ItemGroup
# Create your views here.
from .models import PosProfile
from item.models import Item , Order , OrderLine
import requests
#key = dc71ef8b46b25cd
from django.db.models import Q
from .server_data import *

from item.get_server_item import create_pos_invoice


#90,903.50


def home(request) :
    temp = "base_pos.html"
    
    profile = PosProfile.objects.filter(id =1).first()
   
    entry = OpenEntey.objects.filter(docstatus = "Open").first()
    content =   {
                "profile" : profile ,
                "entry" : entry
                }
    orders = Order.objects.filter(orderstatus = "Open" ,open_entry=entry)
    invoices = Order.objects.filter(orderstatus = "Submited" ,open_entry=entry).count()
    content["invoices"] = invoices
    content["orders"] = orders.count()
    return render(request , temp, content )


def pos_profile(request) :
    content = {"groups" :{} , 'profile' : {}}
    if request.method =='GET' :
        orders = Order.objects.filter(orderstatus = "Open")
        groups = ItemGroup.objects.all()
        profile, created = PosProfile.objects.get_or_create(
        id = 1,
        
             )
        if profile :
            content['profile'] = profile
        content["groups"] =  groups 
        content["orders"] = orders
        return render(request , "home.html" , content )
    if  request.method =='POST' :
        obj, created = PosProfile.objects.get_or_create(
        id = 1,
        
             )
        if obj :
            obj.name=str(request.POST.get('name'))
            obj.appkey=request.POST.get('appkey')
            obj.appsecret=request.POST.get('appsecret')
            obj.pricelist = request.POST.get('pricelist')
            obj.save()

        return redirect('home')



def orders(request ,id, *args, **kwargs ) :
    open_entry = id
    if request.method == "GET" and open_entry:
        order = Order()
        order.customer= "Pos Cutomer"
        order.orderstatus = "Open"
        entry = OpenEntey.objects.get(id = open_entry)
        order.open_entry= entry
        order.save()
        itemgroup = ItemGroup.objects.all()
        profile = PosProfile.objects.filter(id =1).first()
        orders = Order.objects.filter(orderstatus = "Open")
        if not profile.name :
            return redirect ('profile')
        items = Item.objects.all()
        
        content =   {
                "profile" : profile.name if profile else None ,
                "items" : items , 
                "open_orders" : orders,
                "order" : order ,
                "entry" : entry,
              
                }
   
    
        return redirect("edit_order" , order.id)
    else :
        return redirect('main')

def edit_order(request , id ):
    
    profile = PosProfile.objects.filter(id =1).first()
    itemgroup = ItemGroup.objects.all()
    open_entry = OpenEntey.objects.filter(docstatus="Open").first()
    orders = Order.objects.filter(orderstatus = "Open" , open_entry=open_entry)
    order = Order.objects.get(pk = id)
    if not profile.name :
        return redirect ('profile')
    gruop = request.GET.get('Home')
    search_name = request.GET.get('search')
    if gruop :
        items = Item.objects.filter(item_group = gruop)
    else :
       
        items = Item.objects.all()
    if search_name:
        items = Item.objects.filter(Q(item_name__icontains =search_name)|Q(item_code__icontains =search_name))
    content =   {
                "profile" : profile.name if profile else None ,
                "items" : items , 
                "order" : order,
                "open_orders":orders ,
                "entry" : open_entry,
                 "item_group" : itemgroup ,
                 "group": gruop
                }
    
   
    
        

    if request.method == "POST":
        qty = 1
        get_qty = request.POST.get('get_qty')
        if get_qty:
            qty = float(get_qty)
        id_list = order.items.all()
        item_id = request.POST.get("item_id")
        item = Item.objects.get(id = item_id)
        old =  False
        old_id= False 
        for ex_item in id_list :
            
            if str(ex_item.item.id) == str(item_id) :
                old = True
                old_id = ex_item.id
            
        if old and old_id :
            orderline = OrderLine.objects.filter(id =old_id ).first()
            orderline.qty = orderline.qty + qty 
            orderline.save()
            order.save()
        if not old :
            order.items.create(item = item , 
                                price = float(item.pricelist_rate or  0),
                                qty = 1 )
            order.save()

       

    return render (request , "orders.html" ,content)
def remove_item(request) :
    order_id = request.POST.get("orderid")
    order = Order.objects.get(id =int(order_id))
    line_id = request.POST.get("lineid")
    orderline = OrderLine.objects.get(id =int(line_id) )
    orderline.qty = orderline.qty - 1 
    orderline.save()
    if orderline.qty == 0 :
        order.items.remove(orderline)
    
    order.save()
    return redirect('edit_order' , order.id )
def order_details(request , id) :
    # order = Order.objects.get(id =id )
    order = get_object_or_404(Order , pk = id)
    content = {"order" : order}
    return render(request , "orderdetail.html" , content)



def delete_order(request ,id) :
   
        Order.objects.get(id =id).delete()
        return redirect('order-list')



def create_remote_pos(orderid) :
    profile = PosProfile.objects.get(id=1)
    connected = check_connection(profile.appkey, profile.appsecret,profile.server_url)
    if connected :
        succes = create_pos_invoice(profile.server_url ,profile.appkey, profile.appsecret,profile.name ,orderid)
        return succes
    else :
        return False
def submit_order(request ,id) :
       
       order = Order.objects.get(id =id)
       order.orderstatus ="Submited"
       
       for item in order.items.all() :
           item_qty = Item.objects.get(id = item.item.id )
           item_qty.actual_qty = item_qty.actual_qty - item.qty 
           item_qty.save()
       order.save()
       create_remote_pos(order.id )


       return redirect('main')