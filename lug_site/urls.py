from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Wiki views
    url(r'^wiki/', include('lug_wiki.urls')),

    # Events views
    url(r'^events/', include('lug_events.urls')),

    # Profile and account views
    url(r'^', include('lug_people.urls')),

    # Admin interface and other internals
    url(r'^admin/', include(admin.site.urls)),

    # Template index
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
)
