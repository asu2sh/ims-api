from django.shortcuts import render

def home_view(request):
    return render(request, 'inventory_system/home.html')
