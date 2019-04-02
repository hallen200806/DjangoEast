from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse

def login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')

    user = auth.authenticate(username=username, password=password)
    # referer是指之前的页面，如果不存在就通过反向解析跳转到首页
    referer = request.META.get('HTTP_REFERER',reverse('blog:index')) # HTTP_REFERER是请求头的一部分，告诉服务器是从哪里来的
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return redirect(referer) # 重定向到上一个页面
        else:
            return render(request, 'error.html', {'error_message': "登录出错"})
    else:
        return render(request, 'error.html', {'error_message': "用户名或者密码错误"})