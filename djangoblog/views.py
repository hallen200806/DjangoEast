from django.shortcuts import render

def login(request):
    return render(request, 'blog/login.html', {})