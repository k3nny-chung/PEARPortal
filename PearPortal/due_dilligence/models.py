from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Material(models.Model):
	name = models.CharField(max_length = 150, blank = False, null = False)
	description = models.CharField(max_length = 500, blank = True, null = True)
	recycling_rate = models.DecimalField(max_digits = 5, decimal_places = 2, null = True)

	def __str__(self):
		return "%s - %s - %.2f%%" % (self.name, self.description[:20], self.recycling_rate)


class MaterialProcessor(models.Model):
	company_name = models.CharField(max_length = 150, unique = True)
	downstream_process = models.CharField(max_length = 250, blank = True, null = True)
	street_addr = models.CharField(max_length = 250, blank = True, null = True)
	city = models.CharField(max_length = 150, blank = True, null = True)
	zip_code = models.CharField(max_length = 50, blank = True, null = True)
	country = models.CharField(max_length = 50, blank = True, null = True)
	subscribed_users = models.ManyToManyField(User)
	material_types = models.ManyToManyField(Material)
	created = models.DateTimeField(auto_now_add = True)
	last_modified = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.company_name

	class Meta:
		verbose_name = 'processor'
		verbose_name_plural = 'processors'


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
	expiration = models.DateField(null = True)

	def doc_directory_path(instance, filename):
		return "{0}/{1}".format(instance.uploaded_by.username, filename)
		
	upload = models.FileField(upload_to = doc_directory_path)
	original_filename = models.CharField(max_length = 250, blank = True, null = True)

	def __str__(self):
		if self.original_filename:
			return self.original_filename
		else:
			return os.path.basename(self.upload.name)
		


class UserUploadedDocument(models.Model):
	uploaded_by = models.ForeignKey(User, editable=False)
	processor = models.ForeignKey(MaterialProcessor, null = True)
	date_uploaded = models.DateTimeField(auto_now_add = True)

	def doc_directory_path(instance, filename):
		return "{0}/{1}".format(instance.uploaded_by.username, filename)
		
	upload = models.FileField(upload_to = doc_directory_path)
	original_filename = models.CharField(max_length = 250, blank = True, null = True)

	def __str__(self):
		if self.original_filename:
			return self.original_filename
		else:
			return os.path.basename(self.upload.name)


