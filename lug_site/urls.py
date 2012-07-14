from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # General site views
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),

    # Profile and account views
    (r'^', include('lug_people.urls')),

    # Admin interface and other internals
    url(r'^admin/', include(admin.site.urls)),
)
