from django.shortcuts import render,HttpResponse

# Create your views here. Yani url geldigi zaman calistrilicak fonksiyonlar.
# request argumani http requesti.Her view fonksiyonunda bulunmasi lazim.
def index(request):
    return render(request,"home.html")