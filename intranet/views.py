from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from intranet.forms import DocumentForm
from intranet.models import Document
from django.db.models import Q
from login.models import User
from unidecode import unidecode
from django.utils.encoding import smart_str

# Create your views here.


def home(request, search=None):
	if request.user.is_authenticated() == True:
		all_docs = Document.objects.all()
		if search is None: #Si no es una busqueda
			documents = all_docs
		else:
			split_search = unidecode(search.lower()).split(' ', 1)
			documents = []
			for document in all_docs:
				if document.match(split_search):
					documents.append(document)
		parameters = {'current_view': 'intranet', 'documents': documents}
		if search is not None:
			parameters['search'] = search
		return render(request, 'intranet/home.html',parameters)
	else:
		return HttpResponseRedirect(reverse('login'))

def profile(request):
	if request.user.is_authenticated() == True:
		return render(request, 'intranet/profile.html', {'current_view': 'intranet'})
	else:
		return HttpResponseRedirect(reverse('login'))

def upload(request):
	if request.user.is_authenticated() == True:
		if request.method == "GET":
			return render(request, 'intranet/upload.html', {'current_view': 'intranet'})
		else:
			request.POST['owner'] = User.objects.get(email=request.user.email)
			print request.POST['owner']
			form = DocumentForm(request.POST, request.FILES)
			print form.errors
			if form.is_valid():
				final_form = form.save(commit=False)
				final_form.owner = request.user
				final_form.save()
				return HttpResponseRedirect(reverse('upload'))
			else:
				return HttpResponseRedirect(reverse('upload'))
	else:
		return HttpResponseRedirect(reverse('login'))

def pdf_viewer(request, title=None, author=None):
	try:
		document = Document.objects.get(title=title, author=author)
	except Document.DoesNotExist:
		document = None
	if document is not None:
		if ((document.type and document.owner == request.user) or not document.type):
			print '----------------', document.document.url
			#Informacion por 'rb': http://stackoverflow.com/questions/11779246/how-to-show-a-pdf-file-in-a-django-view
			pdf = open(document.document.url, 'rb')
			response =  HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline;filename=some_file.pdf'.replace('some_file',title)
			return response
		else:
			return HttpResponse('Debes tener una cuenta para visualizar este archivo.')
	else:
		return HttpResponse('No se encontraron documentos con el nombre: ' + title)		