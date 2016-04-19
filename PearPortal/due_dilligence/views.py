from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Document
from .forms import DocForm

PAGE_SIZE = 20

@login_required
def doc_index(request):
	#docs = Document.objects.filter(processor__in = request.user.materialprocessor_set.all())
	processors = request.user.materialprocessor_set.all()
	template = loader.get_template('due_dilligence/docIndex.html')
	context = { 
		'processors' : processors, 
	}

	return HttpResponse(template.render(context, request))

@login_required
def user_uploaded_docs(request):
	docs_list = Document.objects.filter(uploaded_by = request.user).order_by('-date_uploaded')
	paginator = Paginator(docs_list, PAGE_SIZE)
	form = DocForm()
	page = request.GET.get('page')
	try:
		docs = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		docs = paginator.page(1)
	except EmptyPage:
		# if page is out of range, deliver the last page
		docs = paginator.page(paginator.num_pages)
			
	return render(request, 'due_dilligence/userDocs.html', { 'documents': docs, 'form': form })


@login_required
def upload_doc(request):
	if request.method == "POST":
		form = DocForm(request.POST, request.FILES)
		if form.is_valid():
			doc = form.save(commit=False)
			doc.uploaded_by = request.user
			form.save()
			return HttpResponseRedirect(reverse('duedilligence:index'))
	else:
		form = DocForm()
	return 	render(request, 'due_dilligence/upload.html', { 'form': form })

@login_required
def upload_doc_xhr(request):
	if request.method == "POST":
		form = DocForm(request.POST, request.FILES)
		if form.is_valid():
			doc = form.save(commit=False)
			doc.uploaded_by = request.user
			form.save()
			return JsonResponse({ 'success': 'true' })
		else:
			return JsonResponse({
					'success': 'false',
					'errors': dict(form.errors.items())
				})


@login_required
def delete_doc_xhr(request, doc_id):
	if request.method == "POST":		
		doc = Document.objects.get(id = doc_id)
		if doc:
			if doc.uploaded_by == request.user:
				doc.delete()
				docs_list = Document.objects.filter(uploaded_by = request.user).order_by('-date_uploaded')
				paginator = Paginator(docs_list, PAGE_SIZE)
				page = request.POST.get('page')
				try:
					docs = paginator.page(page)
				except PageNotAnInteger:
					# if page is not an integer, deliver first page
					docs = paginator.page(1)
				except EmptyPage:
					# if page is out of range, deliver the last page
					docs = paginator.page(paginator.num_pages)

				return render(request, 'due_dilligence/userDocsPartial.html', { 'documents': docs })
			else:
				return HttpResponse('unauthorized', status_code = 401)


