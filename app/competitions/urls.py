from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('competitions.views',
    url(r'^$', 'categories', name='categories'),
    url(r'^competition/(?P<pk>\d+)/$', 'competition', name='competition'),
    url(r'^add_entry/(?P<competition_id>\d+)/$', 'add_entry', name='add_entry'),
    url(r'^results_page/$', 'results_page', name='results_page'),
)
