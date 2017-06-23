from django.shortcuts import render

# Create your views here.
def login(request):
    if request.method == 'POST':
        user = Users.objects.get(id=1)
        uname = request.POST['username']
        response = HttpResponse()
        pwd = md5(request.POST['password']).hexdigest()
        request.POST['password']
        try:
            user = Users.objects.get(username = uname)
        except:
            response.write('<html><script type="text/javascript">alert("1"); window.location="/login"</script></html>')
            return response
        if user.password == pwd:
            request.session['username'] = uname
            return HttpResponseRedirect('/index')
        else:
            response.write('<html><script type="text/javascript">alert("2"); window.location="/login"</script></html>')
            return response     
    return render(request,'login/login.html', locals())
