# -*- coding: utf-8 -*-



from django.conf.urls import *
from sysBasis.views import *


urlpatterns = [
    url(r'^$', login),
    url(r'^login',login)
]