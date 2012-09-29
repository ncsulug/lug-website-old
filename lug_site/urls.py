from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Blog views
    url(r'^', include('lug_blog.urls')),

    # Wiki views
    url(r'^wiki/', include('lug_wiki.urls')),

    # Profile and account views
    url(r'^', include('lug_people.urls')),

    # Admin interface and other internals
    url(r'^admin/', include(admin.site.urls)),
)
