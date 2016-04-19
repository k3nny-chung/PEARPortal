from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import MaterialProcessor, UserProfile, Document


class DocumentAdmin(admin.ModelAdmin):
	
	list_display = ('__str__', 'processor', 'is_published', 'date_uploaded', 'uploaded_by')
	list_filter = ['processor', 'uploaded_by']

	# Make the uploaded_by field read-only on Document creation
	def get_readonly_fields(self, request, obj=None):
		if obj is not None:
			return self.readonly_fields + ('uploaded_by',)

		return self.readonly_fields

	def add_view(self, request, form_url="", extra_context=None):
		data = request.GET.copy()
		data['uploaded_by'] = request.user
		request.GET = data
		return super(DocumentAdmin, self).add_view(request, form_url="", extra_context=extra_context)


class DocumentInline(admin.TabularInline):
	model = Document
	extra = 0
	#fields = ['upload', 'is_published', 'date_uploaded', 'uploaded_by']

	# Select the current admin user as the value for the uploaded_by field
	# def formfield_for_foreignkey(self, db_field, request, **kwargs):
	# 	if db_field.name == 'uploaded_by':
	# 		kwargs['queryset'] = User.objects.filter(username=request.user.username)

	# 	return super(DocumentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

	#Make the uploaded_by field read-only on Document creation
	# def get_readonly_fields(self, request, obj=None):
	# 	if obj:
	# 		return ('uploaded_by',)
	# 	else:	
	# 		return ()

	# def add_view(self, request, form_url="", extra_context=None):
	# 	data = request.GET.copy()
	# 	data['uploaded_by'] = request.user		
	# 	request.GET = data
	# 	return super(DocumentInline, self).add_view(request, form_url="", extra_context=extra_context)

class DocumentReadOnly(DocumentInline):
	fields = ['upload', 'is_published', 'date_uploaded', 'uploaded_by']

	can_delete = True

	def has_add_permission(self, request):
		return False

	def get_readonly_fields(self, request, obj=None):
		return ('processor', 'is_published', 'date_uploaded', 'uploaded_by', 'upload')


class MaterialProcessorAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, { 'fields': ['company_name', 'material', 'subscribed_users'] }),
		('Address', { 'fields': ['street_addr', 'city', 'zip_code', 'country'], 'classes': ['collapse'] }),		
	]
	
	#inlines = (DocumentInline,)
	filter_horizontal = ('subscribed_users',)
	
	def document_count(self, obj):
		return obj.document_set.count()

	document_count.short_description = "Number of Documents"

	list_display = ['company_name', 'material', 'document_count']


	def add_view(self, request, form_url='', extra_context=None):
		self.inlines = []
		return super(MaterialProcessorAdmin, self).add_view(request, form_url, extra_context)

	def change_view(self, request, object_id, form_url='', extra_context=None):
		self.inlines = [DocumentReadOnly,]
		return super(MaterialProcessorAdmin, self).change_view(request, object_id, form_url, extra_context)


class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False

class UserAdmin(BaseUserAdmin):
	inlines	= (UserProfileInline, )

admin.site.register(MaterialProcessor, MaterialProcessorAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.site_header = "PEAR Portal Administration"
admin.site.site_title = "PEAR Site Admin"