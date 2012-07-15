from django.db import models
from django.utils import timezone
from lug_people.models import MemberProfile

class BlogPostManager(models.Manager):
    def active(self):
        return super(BlogPostManager, self).get_query_set().filter(is_active=True)

    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())


class BlogPost(models.Model):
    title           = models.CharField("title", max_length=240,
                        help_text=u"The post's headline.")
    slug            = models.SlugField("slug", unique_for_date='pub_date',
                        help_text=u"This will appear in the post's URL.")
    content         = models.TextField("content")
    author          = models.ForeignKey(MemberProfile, verbose_name="author",
                        help_text=u"The member who wrote the blog post.")
    is_active       = models.BooleanField("is active?", default=False,
                        help_text=u"Whether this post is published or not.")
    pub_date        = models.DateTimeField("publication date",
                        default=timezone.now,
                        help_text=u"When this article is to be published. "
                                  u"(Set it to the future, and it will not "
                                  u"appear until then.)")

    class Meta:
        verbose_name = 'blog post'
        verbose_name_plural = 'blog posts'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    @property
    def is_published(self):
        return self.is_active and self.pub_date < timezone.now()
