from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^parser/$', views.link_parser, name="link_parser"),
    url(r'^folder/$', views.folder_files, name="folder_files"),
    url(r'^folder/(?P<folder_id>.*)/$', views.folder_files, name="folder_files"),
    url(r'^oauth2callback/$', views.oauth2callback, name="oauth2callback"),
    url(r'^get_credentials/$', views.get_credentials, name="get_credentials"),
    url(r'^download/(?P<ids>.*)/$', views.download_drive_files, name="download_drive_files"),
    url(r'^deauthenticate/(?P<redirect>.*)/$', views.deauthenticate, name="deauthenticate"),
]
