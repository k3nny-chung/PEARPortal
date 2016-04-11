from django.conf.urls import url
from . import views

app_name = 'duedilligence'
urlpatterns = [
	url(r'^$', views.doc_index, name='index'),
	url(r'^doc/upload$', views.upload_doc, name='upload'),
	url(r'^api/upload$', views.upload_doc_xhr, name='upload_xhr'),
	url(r'^docs$', views.user_uploaded_docs, name='user_docs'),
]