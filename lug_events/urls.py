from django.conf.urls import patterns, include, url
from .views import EventListView

urlpatterns = patterns('',
    url(r'^$', EventListView.as_view())
)
