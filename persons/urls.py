from django.conf.urls import url
from persons import views

urlpatterns = [
	url(r'^nuevo', views.person_create, name='person_create'),
	url(r'^identificar', views.person_identify, name='person_identify'),
	url(r'^match/$', views.person_identify_by_face, name='person_identify_by_face'),
	url(r'^buscar/$', views.person_search, name='person_search'),
	url(r'^add', views.person_add_cloud, name='person_add_cloud'),#
	url(r'^person-list', views.person_get_cloud, name='person_get_cloud'),#
	url(r'^test', views.person_test, name='person_test'),#
	url(r'^(?P<pk>[0-9]+)/actualizar/$', views.person_update, name='person_update'),
	url(r'^(?P<pk>[0-9]+)/add-face/$', views.person_add_face, name='person_add_face'),
	url(r'^(?P<pk>[0-9]+)/match/$', views.person_verify_by_face, name='person_verify_by_face'),
	url(r'^(?P<pk>[0-9]+)/verificar/$', views.person_verify, name='person_verify'),
	url(r'^(?P<pk>[0-9]+)/$', views.person_detail, name='person_detail'),
	url(r'^', views.person_list, name='person_list'),	
]