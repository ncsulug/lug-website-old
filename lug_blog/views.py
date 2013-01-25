from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
                                        MonthArchiveView, DayArchiveView)
from django.contrib.syndication.views import Feed
from .models import BlogPost


archive_options = dict(
    model = BlogPost,
    queryset = BlogPost.objects.active(),
    date_field = 'pub_date',
    context_object_name = 'posts',
    paginate_by = 10,
    allow_empty = False
)

archive_index = ArchiveIndexView.as_view(**archive_options)
year_archive = YearArchiveView.as_view(make_object_list=True,
                                       **archive_options)
month_archive = MonthArchiveView.as_view(month_format='%m',
                                         **archive_options)
day_archive = DayArchiveView.as_view(month_format='%m',
                                     **archive_options)
post_detail = DetailView.as_view(model = BlogPost,
                                 queryset = BlogPost.objects.published(),
                                 context_object_name='post')



class BlogFeed(Feed):
    title = "LUG @ NC State"
    link = "/feed/"
    description = "Posts from the LUG at NC State University"

    def items(self):
        return BlogPost.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

