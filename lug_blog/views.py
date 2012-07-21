from django.views.generic import DetailView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
                                        MonthArchiveView, DayArchiveView)
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
