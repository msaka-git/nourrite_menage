from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse,get_object_or_404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from .models import nourriture,liesure,list_index
# Create your views here. Yani url geldigi zaman calistrilicak fonksiyonlar.
# request argumani http requesti.Her view fonksiyonunda bulunmasi lazim.
def index(request):
    return render(request,"home.html")

# def file_upload(request):
#     return render(request,'home.html')

def home(request):
    if request.method =="POST" and not request.FILES.keys():

         return render(request,"home.html")
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs= FileSystemStorage()
        file_name = fs.save(uploaded_file.name,uploaded_file)
        url = fs.url(file_name)
        context = {
            "name" : uploaded_file.name,
            "size" : uploaded_file.size,
            "file_url": url,

        }


        return render(request,"home.html",context)
    return render(request,"home.html")

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