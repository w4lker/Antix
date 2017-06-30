# -*- coding:utf-8 -*-  
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from models import *
from md5 import md5
# Create your views here.
def login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        response = HttpResponse()
        pwd = md5(request.POST['password']).hexdigest()
        request.POST['password']
        try:
            user = User.objects.get(username = uname)
        except:
            error = '用户名或密码错误!'
        if user.password == pwd:
            request.session['username'] = uname
            msg = 'success'
            return HttpResponseRedirect('/index')
        else:
            error = '用户名或密码错误!'
            response.write('<html><script type="text/javascript">alert("2"); window.location="/login"</script></html>')
        return render(request,'base/login.html', locals())
    return render(request,'base/login.html', locals())

def index(request):
    return render(request,'base/index.html', locals())

def dashboard(request):
    return render(request,'base/dashboard.html', locals())
    