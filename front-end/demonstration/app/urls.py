from django.conf.urls import url
from app import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    #url(r'^profile/$', views.profile, name='profile'),
    url(r'^hashtagger/$', views.hashtagger, name='hashtagger'),
    url(r'^hashtagger/results/$', views.results, name='results'),

]


