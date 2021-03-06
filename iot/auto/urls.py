"""auto URL Configuration

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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views
from iotdata.views import Feeds, home, overview, analysis, about


urlpatterns = [
    #url(r'^$', RedirectView.as_view(url='home/', permanent=False), name='index'),
    url(r'^$', about, name='about'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'iotdata/login.html'}),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', 'template_name': 'registration/logged_out.html'}, 'logout'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', about, name='about'),
    url(r'^overview/', overview, name='overview'),
    url(r'^analysis/', analysis, name='analysis'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'api/feeds', Feeds.as_view(), name='readings'),
    url(r'^watchman/', include('watchman.urls')),
]

urlpatterns += staticfiles_urlpatterns()
