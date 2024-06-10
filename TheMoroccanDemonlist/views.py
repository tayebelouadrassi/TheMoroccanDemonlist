from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html', {}) 

def guidelines(request):
    return render(request, 'guidelines.html')