from django.conf.urls import patterns, include, url
from .views import (archive_index, year_archive, month_archive, day_archive,
                    post_detail)

YEAR = r'(?P<year>\d{4})/'
MONTH = r'(?P<month>\d{1,2})/'
DAY = r'(?P<day>\w{1,2})/'
SLUG = r'(?P<slug>[\w-]+)/'

urlpatterns = patterns('',
    url('^posts/' + SLUG, post_detail, name='blog_post'),
#    url('^' + YEAR + MONTH + DAY, day_archive, name='blog_day'),
#    url('^' + YEAR + MONTH, month_archive, name='blog_month'),
#    url('^' + YEAR, year_archive, name='blog_year'),
    url('^/?$', archive_index, name='index')
)
