"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('^accounts/', 'django.contrib.auth.views.login', {'template_name': 'core/cover.html'}),
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'core.views.home', name='home'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'core/cover.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', 'bootcamp.auth.views.signup', name='signup'),
    url(r'^settings/$', 'core.views.settings', name='settings'),
    url(r'^settings/picture/$', 'core.views.picture', name='picture'),
    url(r'^settings/upload_picture/$', 'core.views.upload_picture', name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', 'core.views.save_uploaded_picture', name='save_uploaded_picture'),
    url(r'^settings/password/$', 'core.views.password', name='password'),
    url(r'^network/$', 'core.views.network', name='network'),
    url(r'^feeds/', include('feeds.urls')),
    url(r'^questions/', include('questions.urls')),
    url(r'^articles/', include('articles.urls')),
    url(r'^messages/', include('bootcamp.messages.urls')),
    url(r'^notifications/$', 'activities.views.notifications', name='notifications'),
    url(r'^notifications/last/$', 'activities.views.last_notifications', name='last_notifications'),
    url(r'^notifications/check/$', 'activities.views.check_notifications', name='check_notifications'),
    url(r'^notifications/show/$', 'activities.views.show_notifications', name='show_notifications'),
    url(r'^search/$', 'search.views.search', name='search'),
    url(r'^profile/(?P<username>[^/]+)/$', 'core.views.profile', name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
    url(r'^competitions/', include('competitions.urls', namespace='competitions')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
