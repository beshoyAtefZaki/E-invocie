import requests
import json

from requests.api import delete
from .models import Item ,Order ,ItemGroup
from django.shortcuts import render ,redirect ,get_object_or_404
from datetime import datetime

REMOTE_METHOD = '/api/method/dynamicerp.dynamic_erp.point_of_sale.point_of_sale.'

def get_remote_item ( url ,key, secret , pos_profile ,create,*args , **kwargs):
    try :
        if create :
            Item.objects.all().delete()
        headers  =  {
                            'Authorization': "Token %s:%s"%(key,secret)

                    }
        server_url  = str(url) +REMOTE_METHOD +'get_items'
        data = {"pos_profile" : pos_profile}
        req = requests.post(server_url , headers=headers,data=data)
        json_data = json.loads(req.text)
        items = json_data.get('items') 
        for item in items :
            new_item ,careate= Item.objects.get_or_create(
                item_code = item.get('item_code') 

            )
            new_item.item_name = item.get('item_name')
            new_item.item_arabic_name = item.get('description')
            new_item.stock_uom = item.get('stock uom')
            new_item.pricelist_rate = item.get('price_list_rate')
            new_item.actual_qty = item.get('actual_qty')
            new_item.item_group = item.get('item_group')
           
            ex_groups = ItemGroup.objects.all()
            if item.get('item_group') not in [n.name for n in ex_groups] :
                gr = ItemGroup(name = item.get('item_group'))
                gr.save()
            new_item.save()


        return True
    except:
        pass


def create_pos_invoice(url,key,secret ,posprofile,orderid,*args ,**kwargs):
    headers  =  {
                        'Authorization': "Token %s:%s"%(key,secret)

                }
    order = Order.objects.get(id = orderid)
    items = [{"item_code" : str(item.item.item_code ),"qty":str( item.qty) , "price" : str(item.price)} for item in order.items.all()]
    server_url  = str(url) +REMOTE_METHOD +'build_remote_transaction'
    data ={ 'pos_profile':posprofile ,
            'posting_date' : datetime.now(),
            'total': order.total,
            'grand_total': order.grandtotal,
            'items' : json.dumps(items) }

    #create request after init data
    req = requests.post(server_url , headers=headers,data=data)

    
    
    respone = req.text
    inv = json.loads(respone).get('message')
    if inv :
        order.remote_name = inv
        order.synced=True
        order.save()