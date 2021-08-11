from django.shortcuts import render

# Create your views here.


def invoice_list(request):
    return render(request ,'e-invice.html' ) 