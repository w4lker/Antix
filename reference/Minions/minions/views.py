# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db import connection,transaction
from django.core import serializers
from minions.models import *
from manager.settings import *
from hashlib import md5
import sys
import re
import urllib2
import gzip
import StringIO
import string
import base64
import webbrowser
import ast
import datetime
import urlparse
import chardet
import codecs
# Create your views here.
@csrf_protect


def login(request):
    return render(request, 'minions/template/login.html')

def index(request):
    if request.session.get('username') != None:
        menus = Menu.objects.order_by('pri').all()
        return render(request, 'minions/template/index.html',{'menus':menus})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response  

def index_page(request):
    if request.session.get('username') != None:
        title = 'Darshboard'
        logs = Devlog.objects.order_by('-id').all()
        sysinfo = get_sysinfo()
        return render(request, 'minions/template/test_index.html',{'title':title,'logs':logs,'sysinfo':sysinfo})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response
  

def login_check(request):
    user = Users.objects.get(id=1)
    uname = request.POST['username']
    response = HttpResponse()
    pwd = md5(request.POST['password']).hexdigest()
    request.POST['password']
    try:
        user = Users.objects.get(username = uname)
    except:
        response.write('<html><script type="text/javascript">alert("暗号都记不住，你丫还搞啥革命呀！"); window.location="/login"</script></html>')
        return response
    if user.password == pwd:
        request.session['username'] = uname
        return HttpResponseRedirect('/index')
    else:
        response.write('<html><script type="text/javascript">alert("暗号都记不住，你丫还搞啥革命呀！"); window.location="/login"</script></html>')
        return response  

def login_out(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/login')

def test(request):
    request.breadcrumbs([(("homepage"),'/'),  
                         (("activity"),'/activity/')  
                         ])  
    return render(request,'minions/template/test123.html', {'page_title':'just4test'})   

def user_profile(request):
    if request.session.get('username') != None:
        title = '用户管理'        
        return render(request, 'minions/template/user_profile.html',{'username':request.session.get('username'),'title':title})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def user_edit(request):
    response = HttpResponse()
    if request.method == 'GET':
        if request.session.get('username') != None:
            return render(request,'minions/template/user_edit.html',{'page_title':'UserProfile',"username":request.session.get('username')})
        else:
            response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
            return response 
        
    elif request.method == 'POST':
        rsp = {'code':0,'hint':''}
        if request.session.get('username') != None:
            if request.POST['pass'] != '' and request.POST['new_pass'] != '' and request.POST['re_pass'] !='':
                if request.POST['new_pass'] != request.POST['re_pass']:
                    res['hint'] = '请确定两次新密码一致!'
                    response.write('<html><script type="text/javascript">alert("请确定两次新密码一致!");</script></html>')
                    #return response
                else:
                    uname = request.session.get('username')
                    user = Users.objects.get(username = uname)
                    if user.password == md5(request.POST['pass']).hexdigest():
                        user.password = md5(request.POST['new_pass']).hexdigest()
                        user.save()
                        rsp['code'] = 1
                        rsp['hint'] = '修改成功'                       
                            
                    else:
                        rsp['hint'] = '原密码错误'
            else:
                rsp['hint'] = '请将表单填写完整！'          
            
        else:
            rsp['hint'] = '接头暗号：天王盖地虎,小鸡炖蘑菇!'
            response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return JsonResponse(rsp)

def data_proxy(request):
    if request.session.get('username') != None:
        title = '数据详细' 
        data = Proxydata.objects.order_by('-id').all()
        return render(request, 'minions/template/data_proxy.html',{'title':title,'proxydata':data})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def data_details(request,param):
    if request.session.get('username') != None:
        data = Proxydata.objects.get(id=param)
        return render(request, 'minions/template/data_detail.html',{'page_title':'主页','request':data.request,'response':data.response})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response     
    
def data_replay(request):
    print request.POST['request']
    response = http_request(request.POST['request'])
    data = {'response':''}
    data['response'] = response
    return JsonResponse(data)    

def data_split(data):
    r_content=r'\r\n\r\n(.*)'
    r_url=r'\s(.*)\sHTTP/1.1'
    r_headers=r'(.+):\s(.+)'
    content = re.findall(r_content,data)
    url = re.findall(r_url,data)
    header = {}
    headers = re.findall(r_headers,data)
    for h in headers:
        header[h[0]] = h[1]
    
    if content == []:
        content = ['']   
    
    request = {}
    request['url'] = url[0]   #正则匹配返回的是list，取出其中字符串的值
    request['header'] = header
    request['content'] = content[0]
    return request

def http_request(data):
    request = data_split(data)
    try:
        req = urllib2.Request(url= request['url'],headers=request['header'],data=request['content'])
        rsp = urllib2.urlopen(req)
        code = rsp.code
        msg = rsp.msg
        headers = rsp.headers
        if rsp.info().get('Content-Encoding') == 'gzip':
            data = StringIO.StringIO(rsp.read())
            gzip.GzipFile()
            content = gzip.GzipFile(fileobj=data).read()
        else:
            content = rsp.read()
    except urllib2.HTTPError,e:
        code = e.code
        msg = e.msg
        headers = e.headers
        content = e.read()
    except urllib2.URLError,e:
        response = e.reason
        return response
    response = '''HTTP/1.1 %d %s\n%s\n\n%s''' % (code,msg,headers,content)
    return response

def ajax_test(request):
    print request
    response = {'test':'123'}
    return JsonResponse(response)


def settings_menu_list(request):
    if request.session.get('username') != None:
        title = '系统设置' 
        mlist = Menu.objects.all()
        return render(request, 'minions/template/menu_list.html',{'title':title,'mlist':mlist})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response     

def settings_menu_edit(request,param):
    if request.session.get('username') != None:
        if request.method == 'GET':
            menu = Menu.objects.get(id=param)
            fathermenu = Menu.objects.filter(fatherid=0)
            return render(request, 'minions/template/menu_edit.html',{"menu":menu,"action":"菜单编辑","fathermenu":fathermenu})
        elif request.method == 'POST':
            rsp = {'code':0,'hint':''}
            menu = Menu.objects.get(id=request.POST['id'])
            #titles = Menu.objects.exclude(id=request.POST['id']).values('title')
            menu.title=request.POST['title']
            menu.href=request.POST['href']
            menu.fatherid = request.POST['fatherid']
            if request.POST['fatherid'] == '0':
                fathername = '/'
            else:
                fathername = Menu.objects.get(id=request.POST['fatherid']).title
            menu.fathername = fathername
            print fathername
            menu.pri=request.POST['pri']
            menu.save()
            rsp['hint'] = '修改成功!'
            rsp['code'] = 1
            return JsonResponse(rsp)          
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def settings_menu_reload(request):
    if request.session.get('username') != None:
        mlist = {"1":"test","2":"test2"}
        
        data = serializers.serialize('json', Menu.objects.all())
        return JsonResponse(data,safe=False)
        #return render(request, 'minions/template/menu_list.html',{'page_title':'菜单列表','mlist':mlist})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response  
    
def settings_menu_add(request):
    if request.session.get('username') != None:
        if request.method == 'GET':
            fathermenu = Menu.objects.filter(fatherid=0)
            return render(request, 'minions/template/menu_add.html',{"action":"菜单添加","fathermenu":fathermenu})
        elif request.method == 'POST':
            print request.POST['fatherid']
            rsp = {'code':0,'hint':''}
            if request.POST['fatherid'] == '0':
                fname = '/'
                h= '/'
            else:
                fname = Menu.objects.get(id=request.POST['fatherid']).title
                h = request.POST['href']
            try:
                menu = Menu(title=request.POST['title'],href=h,fatherid=request.POST['fatherid'],fathername=fname,pri=request.POST['pri'])
                menu.save()
            except Exception as e:
                rsp['hint'] = e.message
            else:
                rsp['code'] = 1
                rsp['hint'] = "添加成功！"
            finally:
                return JsonResponse(rsp)        
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def settings_menu_del(request,param):
    if request.session.get('username') != None:
        menu = Menu.objects.get(id=param)
        if menu.fatherid == 0:
            submenu = Menu.objects.filter(fatherid=param)
            submenu.delete()
        menu.delete()
        rsp = {'code':1,'hint':"删除成功"}
        return JsonResponse(rsp)       
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def vul_xss_list(request):
    if request.session.get('username') != None:
        title = '漏洞信息' 
        xss = Xsscan.objects.raw('select * from minions_xsscan group by taskid order by id desc')
        return render(request, 'minions/template/vul_xss.html',{'title':title,'xss':xss})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def vul_xss_poc(request,param):
    if request.session.get('username') != None:
        xss = Xsscan.objects.filter(taskid=param)
        return render(request, 'minions/template/xss_poc.html',{'xss':xss})     
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def vul_xss_del(request,param):
    rsp = {'hint':""}
    if request.session.get('username') != None:
        try:
            xss = Xsscan.objects.filter(taskid=param)
            xss.delete()
        except Exception as e:
            rsp['hint'] = e.message
        else:
            rsp['hint'] = "删除成功"
        return JsonResponse(rsp)       
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def vul_sqli_list(request):
    if request.session.get('username') != None:
        title = '漏洞信息' 
        sqli = Sqliscan.objects.order_by('taskid').all()
        return render(request, 'minions/template/vul_sqli.html',{'title':title,'sqli':sqli})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def settings_modules_list(request):
    if request.session.get('username') != None:
        title = '系统设置' 
        settings_list = Settings.objects.all().values('setting','value')
        settings = {}
        for setting in settings_list:
            settings.setdefault(setting['setting'],setting['value'])
        return render(request, 'minions/template/settings_modules_list.html',{'title':title,'settings':settings})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def settings_modules_edit(request):
    if request.session.get('username') != None:
        rsp = {'code':0,'hint':''}
        if request.POST['module'] == 'proxy':
            Settings.objects.filter(setting='proxy_enabled').update(value=request.POST['proxy_enabled'])
            Settings.objects.filter(setting='port').update(value=request.POST['port'])
            
            if request.POST['upstream_enabled'] == 'true':
                Settings.objects.filter(setting='upstream_enabled').update(value=request.POST['upstream_enabled'])
                Settings.objects.filter(setting='upstream_proxy').update(value=request.POST['upstream_proxy'])
            Settings.objects.filter(setting='negative_type').update(value=request.POST['negative_type'])
            Settings.objects.filter(setting='target').update(value=request.POST['target'])
            
        elif request.POST['module'] == 'sqlmap':
            Settings.objects.filter(setting='sqlmap_enabled').update(value=request.POST['sqlmap_enabled'])
            Settings.objects.filter(setting='server').update(value=request.POST['server'])
            Settings.objects.filter(setting='level').update(value=request.POST['level'])
            Settings.objects.filter(setting='risk').update(value=request.POST['risk'])
            
        elif request.POST['module'] == 'xss':
            Settings.objects.filter(setting='xss_enabled').update(value=request.POST['xss_enabled'])
            Settings.objects.filter(setting='heuristic').update(value=request.POST['heuristic'])
            Settings.objects.filter(setting='payloads').update(value=request.POST['payloads'])      
        
        else:
            rsp['hint'] = '修改失败，没有该模块!'
            rsp['code'] = 0
            return JsonResponse(rsp)             
            
        rsp['hint'] = '修改成功!'
        rsp['code'] = 1
        return JsonResponse(rsp)         
        
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 


def logs_developer_add(request):
    if request.session.get('username') != None:
        if request.POST['logs'] !='':
            Devlog(items=request.POST['logs']).save()
            rsp = {'code':''}
            rsp['code'] = 1
            return JsonResponse(rsp)             
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def logs_sysinfo_query(request):
    rsp = get_sysinfo()
    print rsp
    return JsonResponse(rsp)

def get_sysinfo():
    import psutil  
    import os  
    
    sysinfo = {'cpu':0.0,'memory':0.0,'disk':0.0,'sqli':0,'xss':0,'enumeration':0,'fingerprint':0}
    #打印CPU的占用率 
    sysinfo['cpu'] = psutil.cpu_percent(0.5)   
    #本机内存的总占用率
    sysinfo['memory'] = psutil.virtual_memory().percent    
    #本机硬盘的总占用率
    sysinfo['disk'] = psutil.disk_usage('/').percent
    sysinfo['sqli'] = Sqliscan.objects.filter(status='injected').count()
    sysinfo['xss'] = len(list(Xsscan.objects.raw('select * from minions_xsscan group by taskid')))
    return sysinfo

def penetools_csrf(request):
    return render(request,'minions/template/penetools_csrf.html', {'page_title':'just4test'})   
   
def penetools_csrf_semitester(request):
    raw_request = request.POST.get('rawrequest','')
    split_request = data_split(raw_request)
    params = query_split(split_request['content'])
    url_components =urlparse.urlparse(split_request['url'])
    filepath = 'temp/' + url_components[1] + url_components[2].replace('/','_') + '_' + str(datetime.datetime.now())[:19].replace('-','').replace(' ','').replace(':','') + '.html'
    html_file = codecs.open(filepath,'wb','utf-8')
    html_file.write('''<form action=\"''' + split_request['url'] + '''" method="post">\n''')
    for key,value in params.iteritems():
        html_file.write('''<input type="hidden" name="%s" value="%s">''' % (key,value))
    html_file.write('''</form>\n<script>alert(1);document.forms[0].submit();</script>''')
    html_file.close()
    
    path = APP_PATH.replace('\\','\\\\') + '\\\\' + filepath.replace('/','\\\\')

    webbrowser.get('windows-default').open_new(path)
    return JsonResponse({'success':'true'})
    
    
def query_split(postdata):
    if re.search(r'(\{.*\})',postdata) != None:
        params = ast.literal_eval(postdata)
    else:
        params = query_parse(postdata)
    return params

def query_parse(query):
    pairs = query.split('&')
    dict = {}
    for pair in pairs:
        nv = pair.split('=')
        dict[nv[0]] = nv[1] 
    return dict
    
            