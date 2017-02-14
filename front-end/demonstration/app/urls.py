from django.conf.urls import url
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    #url(r'^profile/$', views.profile, name='profile'),
    url(r'^hashtagger/$', views.hashtagger, name='hashtagger'),
    url(r'^hashtagger/results/$', views.results, name='results'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


