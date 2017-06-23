"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static  
from django.conf import settings  
from minions import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', views.login,name='login'),
    url(r'^index_page',views.index_page,name='page'),
    url(r'^index',views.index,name='login'),
    url(r'^login/check',views.login_check,name='login1'),
    url(r'^login/out',views.login_out,name='login1'),
    url(r'^test',views.test,name='login1'),
    url(r'^user/edit',views.user_edit,name='login1'),
    url(r'^user/profile',views.user_profile,name='login1'),
    url(r'^data/proxy',views.data_proxy,name='login1'),
    url(r'^data/replay',views.data_replay,name='login1'),
    url(r'^data/details/(\d+)/$',views.data_details,name='login1'),
    url(r'^settings/menu/list$',views.settings_menu_list,name='settings'),
    url(r'^settings/menu/edit/(\d*)',views.settings_menu_edit,name='settings'),
    url(r'^settings/menu/add',views.settings_menu_add,name='settings'),
    url(r'^settings/menu/del/(\d*)',views.settings_menu_del,name='settings'),
    url(r'^settings/modules/list$',views.settings_modules_list,name='settings'),
    url(r'^settings/modules/edit$',views.settings_modules_edit,name='settings'),
    url(r'^vul/xss/list$',views.vul_xss_list,name='vul'),
    url(r'^vul/xss/poc/(.{32})',views.vul_xss_poc,name='vul'),
    url(r'^vul/xss/del/(.{32})',views.vul_xss_del,name='vul'),
    url(r'^vul/sqli/list$',views.vul_sqli_list,name='vul'),
    #url(r'^vul/sqli/del/(.{16})',views.vul_sqli_del,name='vul'),
    url(r'^logs/developer/add',views.logs_developer_add,name='logs'),
    url(r'^logs/sysinfo/query',views.logs_sysinfo_query,name='logs'),
    url(r'^penetools/csrf$',views.penetools_csrf,name='logs'),
    url(r'^penetools/csrf/semitester$',views.penetools_csrf_semitester,name='logs'),
    url(r'^ajax_test$',views.ajax_test,name='login1'),
    url(r'^\s?\s?$',views.index,name='login'),
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)  