from django.conf.urls import patterns, include, url
from .views import view_page, edit_page, page_history

TITLE = '(?P<title>[^/]+)'
REVISION_ID = '(?P<revision_id>[0-9]+)'

urlpatterns = patterns('',
    url('^$',                       view_page, {'title': "Home"},
                                    name='wiki_home'),
    url('^' + TITLE + '/$',         view_page, name='wiki_view'),
    url('^' + TITLE + '/edit/$',    edit_page, name='wiki_edit'),
    url('^' + TITLE + '/history/$', page_history, name='wiki_history'),
    url('^' + TITLE + '/history/' +
              REVISION_ID + '/$',   view_page, name='wiki_revision')
)
