from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('feeds.views',
    url(r'^$', 'feeds', name='feeds'),
    url(r'^(\d+)/$', 'feed', name='feed'),
    url(r'^post/$', 'post', name='post'),
    url(r'^post_fb/$', 'post_fb', name='post_fb'),
    url(r'^list/$', 'list', name='list'),
    url(r'^direct_upload_complete/$', 'direct_upload_complete', name='direct_upload_complete'),
    url(r'^upload_prompt/$', 'upload_prompt', name='upload_prompt'),
    url(r'^like/$', 'like', name='like'),
    url(r'^comment/$', 'comment', name='comment'),
    url(r'^load/$', 'load', name='load'),
    url(r'^check/$', 'check', name='check'),
    url(r'^load_new/$', 'load_new', name='load_new'),
    url(r'^update/$', 'update', name='update'),
    url(r'^track_comments/$', 'track_comments', name='track_comments'),
    url(r'^remove/$', 'remove', name='remove_feed'),
    url(r'^upload_image/$', 'upload_image', name='upload_image'),
    url(r'^upload_video/$', 'upload_video', name='upload_video'),
    url(r'^(?P<pk>[0-9]+)/update/$', 'feed_edit', name='feed_edit'),
)