from django.conf.urls import url
from django.views.generic import TemplateView

from app import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^hashtagger/$', views.hashtagger, name='hashtagger'),
    url(r'^hashtagger/uploadaction/$', views.uploadaction, name='uploadaction'),

]

