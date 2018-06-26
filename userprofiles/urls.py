from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^login/$', views.auth_copresa, name='authentication'),
	url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^home/$', views.auth_dashboard, name='home'),	
	url(r'^$', views.auth_home, name='init_view'),	
]