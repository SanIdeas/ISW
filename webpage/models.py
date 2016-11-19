from __future__ import unicode_literals
from django.utils.text import slugify
from django.conf import settings
from login.models import User
from django.db import models
import os


# Create your models here.
class Section(models.Model):
	name = models.CharField(max_length=20, unique=True, null=False)
	slug = models.SlugField(max_length=20, unique=True, null=False)
	spanish_title = models.CharField(max_length=200, null=False)
	spanish_body = models.TextField(null=True)
	english_title = models.CharField(max_length=200, null=False)
	english_body = models.TextField(null=True)

	def save(self, *args, **kwargs):
		if not self.id:
			if not self.slug:
				self.slug = slugify(self.name)
			if not self.english_title:
				self.english_title = self.spanish_title
			if not self.english_body:
				self.english_body = self.spanish_body

		super(Section, self).save(*args, **kwargs)

class News(models.Model):
	title = models.CharField(max_length=200, null=True)
	title_html = models.CharField(max_length=200, null=True)
	slug = models.SlugField(max_length=200, null=True)
	body = models.TextField()
	date = models.DateField(null=True, auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	source_text = models.CharField(max_length=200, null=True)
	source_url = models.CharField(max_length=200, null=True)
	is_published = models.BooleanField(default=False)
	admin_annotation = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=200, null=True)
	mini_description = models.CharField(max_length=100, null=True)
	thumbnail = models.FileField(upload_to='static/webpage/images/news/thumbnail/', max_length=500, null=True)
	header = models.FileField(upload_to='static/webpage/images/news/header/', max_length=500, null=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(News, self).save(*args, **kwargs)
	def set_header_filename(self):
		filename_h = 'static/webpage/images/news/header/NH' + str(self.id) + '.jpg'
		os.rename(self.header.path, filename_h)
		self.header.name = filename_h
		self.save()
	def set_thumbnail_filename(self):
		filename_t = 'static/webpage/images/news/thumbnail/NT' + str(self.id) + '.jpg'
		os.rename(self.thumbnail.path, filename_t)
		self.thumbnail.name = filename_t
		self.save()
	def thumbnail_url(self):
		return 'webpage/images/news/thumbnail/' + os.path.basename(self.thumbnail.name)
	def header_url(self):
		return 'webpage/images/news/header/' + os.path.basename(self.header.name)

class Image(models.Model):
	picture = models.FileField(upload_to='static/webpage/images/news/', max_length=500, null=True)
	news = models.ForeignKey(News, on_delete=models.CASCADE)

	def static_url(self):
		return '/' + self.picture.name

	def set_filename(self):
		filename = 'static/webpage/images/news/N' + str(self.news.id) + 'P' + str(self.id) + '.jpg'
		os.rename(self.picture.path, filename)
		self.picture.name = filename
		self.save()