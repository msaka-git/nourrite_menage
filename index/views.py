from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse,get_object_or_404
from django.urls import reverse

from .models import nourriture,liesure
# Create your views here. Yani url geldigi zaman calistrilicak fonksiyonlar.
# request argumani http requesti.Her view fonksiyonunda bulunmasi lazim.
def index(request):
    return render(request,"home.html")

def home(request):
    all_data = nourriture.objects.filter()
    context = {
        "all_data" : all_data
    }
    return render(request,"home.html",context)

def food(request):
    all_data = nourriture.objects.filter()
    total_spent=[i.nourriture_spent for i in all_data]
    sum_spent=round(sum(total_spent),2)
    context = {
             "all_data" : all_data,
             "sum_spent" : sum_spent
    }

    return render(request,"food.html",context)

def liesure_(request):
    all_data = liesure.objects.filter()
    total_spent=[i.liesure_spent for i in all_data]
    sum_spent=round(sum(total_spent),2)
    context = {
            "all_data" : all_data,
            "sum_spent" : sum_spent
    }

    return render(request,"liesure.html",context)

def update(request,id,instance):

    #data = nourriture.objects.filter(id = id)
    data = get_object_or_404(nourriture,id = id) # sayfa yoksa 404 firlatir.
    return_url = "/"+instance
    return render(request,"update.html",{"data": data,"return_url":return_url})

def delete_row(request):
    pass