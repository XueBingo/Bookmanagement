"""Bookmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from . import view
 
urlpatterns = [
    #url(r'^hello$', view.hello),
    url(r'^login', view.login),
    url(r'^logout', view.logout),
    url(r'^insertuser', view.insertuser),
    url(r'^showallusers', view.showallusers),
    url(r'^updateuserinfo', view.updateuserinfo),
    url(r'^searchbook', view.searchbook),
    url(r'^updatebookinfo', view.updatebookinfo),
    url(r'^index', view.index),
    url(r'^orderbook', view.orderbook),
    url(r'^purchaseorder', view.purchaseorder),
    url(r'^pay', view.pay),
    url(r'^returnorder', view.returnorder),
    url(r'^addstock', view.addstock),
    url(r'^sellbook', view.sellbook),
    url(r'^checkrecord', view.checkrecord),
    url(r'^showbook', view.salesorder),
]


