from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio/index.html')