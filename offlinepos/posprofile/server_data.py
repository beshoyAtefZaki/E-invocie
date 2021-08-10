import requests 
import json

# from requests.models import requote_uri 
from item.models import ItemGroup


SERVER_URL = '/api/method/dynamicerp.dynamic_erp.point_of_sale.point_of_sale.'




def check_connection(key , secret , durl ) :
    headers  =  {
					    'Authorization': "Token %s:%s"%(key,secret)

		    	}
    url = str(durl) +SERVER_URL+ 'check_connection'
    
    try : 
        req = requests.get(url , headers=headers)
        data = json.loads(req.text)
        return (data)
       
           
    except :
        return False


def get_pos_info(durl , key , secret,profile ):
    headers  =  {
					    'Authorization': "Token %s:%s"%(key,secret)

		    	}
    connect = check_connection(key,secret,durl)
    print(connect)
    if connect :
        url = str(durl) +SERVER_URL+ 'get_pos_profile_details'

        data = {"pos_profile" : profile}

        req = requests.post(url , headers=headers,data=data)
        respone = json.loads(req.text)
        print("res", respone)
        return respone.get('data')


def create_open_entry(serverurl , key , secret , posprofile ,*args, **kwargs):
    url = str(serverurl) + SERVER_URL +'create_opening_voucher'
    headers  =  {
					    'Authorization': "Token %s:%s"%(key,secret)
		    	}

    
    data =  {
                "pos_profile": posprofile ,
                "balance_details": []

            }


    req = requests.post(url , headers=headers,data=data)
    data = json.loads(req.text)
    main = data.get('new_pos_opening').get('name')
    return main