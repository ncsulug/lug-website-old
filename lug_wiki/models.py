from django.db import models
from django.utils import timezone
from lug_people.models import MemberProfile

class Page(models.Model):
    ACCESS_CHOICES = (
        (u"public",     u"Public"),
        (u"protected",  u"Protected"),
        (u"private",    u"Private")
    )

    title           = models.CharField("title", max_length=32, unique=True,
                        help_text=u"This is the page title. It will appear "
                                   "in the URL and at the top of the page.")
    access_level    = models.CharField("access level", max_length=16,
                        choices=ACCESS_CHOICES, default=u"public",
                        help_text=u"Public: anyone can view, any member can "
                                   "edit. Protected: anyone can view, only "
                                   "officers can edit. Private: only "
                                   "officers can view and edit.")

    class Meta:
        ordering = ["title"]
        permissions = (
            ("is_officer",      u"Has officer access to the wiki"),
        )

    def __unicode__(self):
        return self.title

    @property
    def latest_revision(self):
        try:
            return self.revisions.order_by("-timestamp")[0]
        except IndexError:
            return None

    @property
    def last_updated(self):
        rev = self.latest_revision
        return None if rev is None else rev.timestamp

    @property
    def last_updated_by(self):
        rev = self.latest_revision
        return None if rev is None else rev.author

    def user_may_view(self, user):
        if self.access_level == u"private":
            return user.has_perm("lug_wiki.is_officer")
        else:
            return True

    def user_may_edit(self, user):
        if self.access_level == u"public" and user.is_active:
            return True
        else:
            return user.has_perm("lug_wiki.is_officer")


class Revision(models.Model):
    page            = models.ForeignKey(Page, verbose_name="page",
                        related_name="revisions")
    author          = models.ForeignKey(MemberProfile, verbose_name="author")
    content         = models.TextField("content")
    change_note     = models.CharField("change note", max_length=140,
                        help_text=u"Notes about the changes you made.")
    timestamp       = models.DateTimeField("timestamp", default=timezone.now,
                        help_text=u"The time this revision was made.")

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]

    def __unicode__(self):
        return u"%s revision %d" % (self.page.title, self.id)
