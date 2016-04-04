"""demo1 URL Configuration

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
from django.conf.urls import include, url,patterns
from django.contrib import admin
from todolist import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += patterns("",
    url(r'^warning/$', views.warning, name="warning"),
    url(r'^index/$', views.index, name="index"),
    url(r'^add/$', views.add, name="add"),
    url(r'^edit/$', views.edit, name="edit"),
    url(r'^delete/$', views.delete, name="delete"),
    url(r'^done/$', views.done, name="done"),
    url(r'^login/$', views.do_login, name="login"),
    url(r'^logout/$', views.do_logout, name="logout"),
    url(r'^reg/$', views.do_reg, name="reg"),
    url(r'^edit_pass/$', views.edit_pass, name="edit_pass"),
)
