from django.shortcuts import render

# Create your views here.

def guidelines(request):
    return render(request, 'guidelines.html')