from django.conf.urls import url
from . import views

app_name = 'duedilligence'
urlpatterns = [
	url(r'^$', views.dasboard, name='dashboard'),
	url(r'^processors$', views.doc_index, name='index'),
	url(r'^doc/upload$', views.upload_doc, name='upload'),
	url(r'^api/upload$', views.upload_doc_xhr, name='upload_xhr'),
	url(r'^docs$', views.user_uploaded_docs, name='user_docs'),
	url(r'^doc/(?P<doc_id>[0-9]+)/delete$', views.delete_doc_xhr, name='delete_doc_xhr'),
]