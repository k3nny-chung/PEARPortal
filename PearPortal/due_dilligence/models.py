from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class MaterialProcessor(models.Model):
	material = models.CharField(max_length = 150)
	company_name = models.CharField(max_length = 150, unique = True)
	street_addr = models.CharField(max_length = 250, blank = True, null = True)
	city = models.CharField(max_length = 150, blank = True, null = True)
	zip_code = models.CharField(max_length = 50, blank = True, null = True)
	country = models.CharField(max_length = 50, blank = True, null = True)
	subscribed_users = models.ManyToManyField(User)
	created = models.DateTimeField(auto_now_add = True)
	last_modified = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.company_name


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
	company_name = models.CharField(max_length = 150)
	street_addr = models.CharField(max_length = 250, blank = True, null = True)
	city = models.CharField(max_length = 150, blank = True, null = True)
	zip_code = models.CharField(max_length = 50, blank = True, null = True)
	country = models.CharField(max_length = 50, blank = True, null = True)

	def __str__(self):
		return "{0} from {1}".format(self.user.username, self.company_name)


class Document(models.Model):
	uploaded_by = models.ForeignKey(User, editable=False)
	processor = models.ForeignKey(MaterialProcessor, null = True)
	is_published = models.BooleanField('Published?', default = False)
	date_uploaded = models.DateTimeField(auto_now_add = True)

	def doc_directory_path(instance, filename):
		return "{0}/{1}".format(instance.uploaded_by.username, filename)
		
	upload = models.FileField(upload_to = doc_directory_path)

	def __str__(self):
		return os.path.basename(self.upload.name)

	

