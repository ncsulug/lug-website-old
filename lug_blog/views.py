from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
                                        MonthArchiveView, DayArchiveView,
                                        DateDetailView)
from .models import BlogPost

global_options = dict(
    model = BlogPost,
    queryset = BlogPost.objects.active(),
    date_field = 'pub_date'
)

archive_options = global_options.copy()
archive_options.update(
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
post_detail = DateDetailView.as_view(month_format='%m',
                                     context_object_name='post',
                                     **global_options)
