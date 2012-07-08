from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from lug_people.views import ProfileView, ProfileEditView

admin.autodiscover()

urlpatterns = patterns('',
    # General site views
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    # Profile views
    url(r'^~(?P<username>[a-zA-Z0-9@+.-]+)/$',
        ProfileView.as_view(template_name='profiles/show.html'),
        name='profile'),
    url(r'^edit-profile/$',
        ProfileEditView.as_view(template_name='profiles/edit.html'),
        name='profile_edit'),
    # Admin interface and other internals
    url(r'^admin/', include(admin.site.urls)),
)
