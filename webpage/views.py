# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from datetime import datetime, date, timedelta
from intranet.models import Document
from webpage.models import Section, SubSection, News, Member, Event, EventDay, GalleryPhoto
from webpage.forms import ImageForm, NewsCommentForm
from itertools import izip_longest
import json

# Junta elementos de un objeto iterable en grupos de n elementos
# http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def grouped(iterable, n):
	return izip_longest(*[iter(iterable)]*n)

# Create your views here.
def home(request):
	if request.user.is_authenticated():
		if request.user.is_admin:
			exclude = ['intranet', 'publications']
		else:
			exclude = ['administrator', 'publications']
	else:
		exclude = ['intranet', 'administrator']

	documents = Document.objects.filter(is_public=True)[:3]
	sections = Section.objects.all()
	section = Section.objects.get(slug='.')

	eventsId = EventDay.objects.filter(day__gte=datetime.today()).order_by('-day').values_list('event', flat=True).distinct()
	events = Event.objects.filter(id__in=eventsId)
	events_sort = sorted(events, key=lambda event: event.get_date())

	return render(request, 'webpage/home.html', {
							'current_view': section,
							'current_section': section,
							'documents': documents,
							'sections': sections.exclude(slug__in=exclude),
							'body': 'inicio',
							'header': News.objects.filter(in_header=True, is_published=True).exclude(header="").exclude(header=None).order_by('-date')[:5],
							'news_1': News.objects.filter(is_published=True).exclude(thumbnail="").exclude(thumbnail=None).order_by('-date')[:2],
							'news_2': News.objects.filter(is_published=True).exclude(thumbnail="").exclude(thumbnail=None).order_by('-date')[2:4],
							'events': events_sort[:3],
							})


def section(request, section_slug=None, subsection_slug=None):
	if request.user.is_authenticated():
		if request.user.is_admin:
			exclude = ['intranet', 'publications']
		else:
			exclude = ['administrator', 'publications']
	else:
		exclude = ['intranet', 'administrator']

	sections = Section.objects.all()
	if subsection_slug is None:		# Section
		section = get_object_or_404(Section, slug=section_slug)
		categories_arr = []
		categories = section.get_categories()
		for category in categories:
			categories_arr.append((category, category.get_subsections()))

		cat_num = len(categories_arr)
		if cat_num % 2 == 0:	# Pairwise array
			categories_arr = zip(categories_arr, categories_arr[1:])[::2]
		else:
			categories_temp = zip(categories_arr, categories_arr[1:])[::2]
			categories_temp.append((categories_arr[-1], ()))
			categories_arr = categories_temp

		return render(request, 'webpage/section.html', {
								'current_view': section,
								'current_section': section,
								'sections': sections.exclude(slug__in=exclude),
								'body': 'seccion',
								'categories': categories_arr,
								'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3]
								})
	else:		# Subsection
		section = get_object_or_404(Section, slug=section_slug)
		subsection = get_object_or_404(SubSection, slug=subsection_slug)

		if section_slug == 'about' and subsection_slug == 'us':
			return render(request, 'webpage/members.html', {
			'current_view': subsection,
			'current_section': section,
			'current_subsection': subsection,
			'sections': sections.exclude(slug__in=exclude),
			'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3],
			'working': Member.objects.filter(working=True),
			'not_working': Member.objects.filter(working=False),
			})	
		return render(request, 'webpage/subsection.html', {
			'current_view': subsection,
			'current_section': section,
			'current_subsection': subsection,
			'sections': sections.exclude(slug__in=exclude),
			'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3]
		})


def array2d(elements):
	elements_arr = []
	for element in elements:
		elements_arr.append(element)

	ele_num = len(elements_arr)
	if ele_num % 2 == 0:	# Pairwise array
		elements_arr = zip(elements_arr, elements_arr[1:])[::2]
	else:
		elements_temp = zip(elements_arr, elements_arr[1:])[::2]
		elements_temp.append((elements_arr[-1], ()))
		elements_arr = elements_temp
	return elements_arr

def news_feed(request):
	if request.user.is_authenticated():
		if request.user.is_admin:
			exclude = ['intranet', 'publications']
		else:
			exclude = ['administrator', 'publications']
	else:
		exclude = ['intranet', 'administrator']

	sections = Section.objects.all()
	section = Section.objects.get(slug='news')

	paginator = Paginator(News.objects.filter(is_published=True).order_by('-date'), 8)

	# Se extrae el numero de pagina
	if request.GET.get('page'):
		try: news = paginator.page(request.GET.get('page'))
		except: news = paginator.page(1)
	else:
		news = paginator.page(1)
	news_group = grouped(news, 2)

	eventsId = EventDay.objects.filter(day__gte=datetime.today()).order_by('-day').values_list('event', flat=True).distinct()
	events = Event.objects.filter(id__in=eventsId)
	events_sort = sorted(events, key=lambda event: event.get_date())

	return render(request, 'webpage/news_feed.html', {
							'current_view': section,
							'current_section': section,
							'sections': sections.exclude(slug__in=exclude),
							'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3],
							'body': 'seccion',
							'news': news_group if len(news) else None,
							'paginator': news,
							'events': events_sort,
							})


def news_editor(request, id = None):
	if request.user.is_authenticated() and not request.user.is_admin:
		news = News.objects.filter(id=id)
		if news:
			news = news[0]
			if request.method == "GET":
				# Si la noticia corresponde al usuario o es un administrador se permite el acceso
				if news.author == request.user or request.user.is_admin:
					if news:
						if request.user.is_authenticated():
							if request.user.is_admin:
								exclude = ['intranet', 'publications']
							else:
								exclude = ['administrator', 'publications']
							# Se actualizan los comentarios leidos
							news.read_comments(request.user)
						else:
							exclude = ['intranet', 'administrator']

						sections = Section.objects.all()
						section = Section.objects.get(slug='news')

						if news.title:
							title = news.title
						else:
							title = 'Noticia sin título'
						return render(request, 'webpage/news_editor.html', {
												'current_view': Section(spanish_name=title, english_name=title),
												'current_section': section,
												'sections': sections.exclude(slug__in=exclude),
												'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3],
												'body': 'blog',
												'news': news
												})
				else:
					return HttpResponseRedirect(reverse('webpage:home')) # 'No tienes permiso para modificar esta noticia'
			elif request.method == "POST":
				# En este caso la respuesta sera en un objeto JSON
				if request.POST.get('news-title-html') is not None:
					print request.POST.get('news-title-html')
					news.title_html = request.POST.get('news-title-html') if (request.POST.get('news-title') != "" and request.POST.get('news-title') != "undefined") else '<h1 class="c12">' + _(u"Noticia sin título") + '</h1>'
				if request.POST.get('news-title') is not None:
					news.title = ' '.join(request.POST.get('news-title').split()) if (request.POST.get('news-title') != "" and request.POST.get('news-title') != "undefined")  else _(u"Noticia sin título")
				if request.POST.get('news-content') is not None:
					news.body = request.POST.get('news-content')
				news.in_header	 = False
				news.is_published = False
				news.save()
				return JsonResponse({'error': False})
		else:
			# La noticia no existe
			# Deberia enviar al feed de noticias o a una pagina 404
			return HttpResponseRedirect(reverse('webpage:home'))

	else:
		if request.user.is_admin:
			return HttpResponseRedirect(reverse('admin:news'))	
		return HttpResponseRedirect(reverse('webpage:home'))


def news(request, year = None, month = None, day = None, title = None, id = None):
	try:
		if year and month and day and title:
			date = datetime.strptime(str(day) + str(month) + str(year), '%d%m%Y')
			news = News.objects.filter(date=date, slug=title)
		else:
			news = News.objects.filter(id=id)
		if news:
			if request.user.is_authenticated():
				if request.user.is_admin:
					exclude = ['intranet', 'publications']
				else:
					exclude = ['administrator', 'publications']
				# Se actualizan los comentarios leidos
				news[0].read_comments(request.user)
			else:
				exclude = ['intranet', 'administrator']

			sections = Section.objects.all()
			section = Section.objects.get(slug='news')

			if news[0].title:
				title = news[0].title
			else:
				title = 'Noticia sin título'

			return render(request, 'webpage/news.html', {
									'current_view': Section(spanish_name=title, english_name=title),
									'current_section': section,
									'sections': sections.exclude(slug__in=exclude),
									'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3],
									'body': 'blog',
									'news_': news[0],
									'recents': News.objects.filter(is_published=True).exclude(thumbnail="").exclude(thumbnail=None).exclude(id=news[0].id).order_by('-date')[:4],
									})
		else:
			return HttpResponseRedirect(reverse('webpage:news_feed'))
	except Exception as error:
		print error
		return HttpResponseRedirect(reverse('webpage:news_feed'))


def new_news_comment(request):
	news = None
	editor_redirect = 'ret=' + request.GET.get('ret') if request.GET.get('ret') else ''
	if request.POST.get('id'):
		news = News.objects.filter(id=request.POST.get('id'))

	if news:
		news = news[0]
	else:
		return HttpResponseRedirect(reverse('intranet:news'))
	if request.user.is_authenticated() and (news.author == request.user or request.user.is_admin):

		# Se define la url de redireccionamiento
		if request.GET.get('redirect') == 'news':
			dir = reverse('webpage:news', kwargs={'id': news.id})
		else:
			dir = reverse('webpage:news_editor', kwargs={'id': news.id})

		fields = {
			'news': news.id,
			'author': request.user.id,
			'content': request.POST.get('content')
		}
		form = NewsCommentForm(fields)
		if form.is_valid():
			form = form.save()
			return HttpResponseRedirect( '%s%s#comment%s' % (dir, ('?' + editor_redirect if editor_redirect else '') , form.id))
		else:
			print form.errors
			return HttpResponseRedirect( '%s?error=true%s#comments' % (dir, '&' + editor_redirect))
	else:
		if news:
			return HttpResponseRedirect(dir)
		else:
			return HttpResponseRedirect(reverse('webpage:news_feed'))


def save_images(request):
	if request.user.is_authenticated() and request.method == 'POST':
		info = json.loads(request.POST.get('info'))
		news = News.objects.filter(id=info['news_id'])
		if news:
			if news[0].author == request.user or request.user.is_admin:
				response = []
				for key in request.FILES:
					fields = {
							'news': info['news_id']
						}
					files = {
							'picture': request.FILES[key]
						}
					form = ImageForm(fields, files)
					if form.is_valid():
						image = form.save()
						image.set_filename()
						response.append({'client_side_id': key, 'url': image.static_url()})
					else:
						return JsonResponse({'error': True, 'message': form.errors})
				return JsonResponse({'error': False, 'urls': response})
			else:
				return JsonResponse({'error': True, 'message': _("No tienes permisos para modificar esta noticia")})
		else:
			return JsonResponse({'error': True, 'message': _("Esta noticia no existe")})
	else:
		return JsonResponse({'error': True, 'urls': _(u"Debes iniciar sesión")})

def events_feed(request):
	today = datetime.today()
	if request.user.is_authenticated():
		if request.user.is_admin:
			exclude = ['intranet', 'publications']
		else:
			exclude = ['administrator', 'publications']
	else:
		exclude = ['intranet', 'administrator']

	sections = Section.objects.all()
	section = Section.objects.get(slug='events')

	if request.GET.get('year') and request.GET.get('month') and request.GET.get('day'):
		eventsId = EventDay.objects.filter(day__year=request.GET.get('year'), day__month=request.GET.get('month'), day__day=request.GET.get('day')).values_list('event', flat=True).distinct()
		events = Event.objects.filter(id__in=eventsId)
	elif request.GET.get('month'):
		eventsId = EventDay.objects.filter(day__year=datetime.today().year, day__month=request.GET.get('month')).values_list('event', flat=True).distinct()
		events = Event.objects.filter(id__in=eventsId)
	elif request.GET.get('week'):
		start = today - timedelta(days=today.weekday())
		end = start + timedelta(days=6)
		eventsId = EventDay.objects.filter(day__range=[start, end]).values_list('event', flat=True).distinct()
		events = Event.objects.filter(id__in=eventsId)
	else:
		eventsId = EventDay.objects.filter(day__gte=today).values_list('event', flat=True).distinct()
		events = Event.objects.filter(id__in=eventsId)
	events_sort = sorted(events, key=lambda event: event.get_date())
	months = '["'
	for i in range(1, 13):
		months += _(date(2016, i, 12).strftime('%B')) + ('","' if i != 12 else "")
	months += '"]'

	paginator = Paginator(events_sort, 8)

	# Se extrae el numero de pagina
	if request.GET.get('page'):
		try: events_sort = paginator.page(request.GET.get('page'))
		except: events_sort = paginator.page(1)
	else:
		events_sort = paginator.page(1)

	# Se cuentan la cantidad de eventos por dia
	events_counter = {}
	eventsDays = EventDay.objects.all()
	print len(eventsDays)
	for event in eventsDays:
		if str(event.day.year) not in events_counter:
			events_counter[str(event.day.year)] = {}
		if str(event.day.month) not in events_counter[str(event.day.year)]:
			events_counter[str(event.day.year)][str(event.day.month)] = {}
		if str(event.day.day) not in events_counter[str(event.day.year)][str(event.day.month)]:
			events_counter[str(event.day.year)][str(event.day.month)][str(event.day.day)] = 0
		events_counter[str(event.day.year)][str(event.day.month)][str(event.day.day)] += 1

	return render(request, 'webpage/events_feed.html', {
								'current_view': section,
								'current_section': section,
								'sections': sections.exclude(slug__in=exclude),
								'body': 'eventos',
								'today': datetime.today(),
								'events': events_sort,
								'paginator': events_sort,
								'counter': events_counter,
								'months': months,
								'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3]
								})

def event(request, title):
	event_ = Event.objects.filter(slug=title)
	if not event_:
		return HttpResponseRedirect(reverse('webpage:events_feed'))
	if request.user.is_authenticated():
		if request.user.is_admin:
			exclude = ['intranet', 'publications']
		else:
			exclude = ['administrator', 'publications']
	else:
		exclude = ['intranet', 'administrator']

	sections = Section.objects.all()
	section = Section.objects.get(slug='events')

	months = '["'
	for i in range(1, 13):
		months += _(date(2016, i, 12).strftime('%B')) + ('","' if i != 12 else "")
	months += '"]'

	

	# Se cuentan la cantidad de eventos por dia
	events_counter = {}
	eventsDays = EventDay.objects.all()
	print len(eventsDays)
	for event in eventsDays:
		if str(event.day.year) not in events_counter:
			events_counter[str(event.day.year)] = {}
		if str(event.day.month) not in events_counter[str(event.day.year)]:
			events_counter[str(event.day.year)][str(event.day.month)] = {}
		if str(event.day.day) not in events_counter[str(event.day.year)][str(event.day.month)]:
			events_counter[str(event.day.year)][str(event.day.month)][str(event.day.day)] = 0
		events_counter[str(event.day.year)][str(event.day.month)][str(event.day.day)] += 1

	return render(request, 'webpage/event.html', {
								'current_view': section,
								'current_section': section,
								'sections': sections.exclude(slug__in=exclude),
								'body': 'eventos',
								'today': datetime.today(),
								'counter': events_counter,
								'event': event_[0],
								'months': months,
								'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3]
								})

def gallery(request):
	if request.user.is_authenticated():
		if request.user.is_admin:
			exclude = ['intranet', 'publications']
		else:
			exclude = ['administrator', 'publications']
	else:
		exclude = ['intranet', 'administrator']

	sections = Section.objects.all()
	section = Section.objects.get(slug='about')
	subsection = SubSection.objects.get(slug='gallery')

	eventsId = EventDay.objects.filter(day__gte=datetime.today()).order_by('-day').values_list('event', flat=True).distinct()
	events = Event.objects.filter(id__in=eventsId)
	events_sort = sorted(events, key=lambda event: event.get_date())

	return render(request, 'webpage/gallery.html', {
								'current_view': subsection,
								'current_section': section,
								'current_subsection': subsection,
								'sections': sections.exclude(slug__in=exclude),
								'body': 'blog',
								'photos': GalleryPhoto.objects.all(),
								'recents': News.objects.filter(is_published=True).exclude(thumbnail="").exclude(thumbnail=None).order_by('-date')[:4],
								'events': events_sort,
								'other_sections': sections.exclude(slug__in=['.', 'publications', 'intranet', 'administrator', section.slug])[:3]
								})