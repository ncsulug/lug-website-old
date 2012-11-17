import re
from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils import timezone
import urllib

NON_USERNAME_CHARS = re.compile(r'[^\w@+.-]+')


class MemberProfile(models.Model):
    PREFERRED_NAME_CHOICES = (
        (u"nick",   u"Nickname"),
        (u"real",   u"Real Name"),
    )

    ROLE_CHOICES = (
        (u"student",    u"Student"),
        (u"alumnus",    u"Alumnus"),
        (u"faculty",    u"Faculty"),
        (u"staff",      u"Staff"),
        (u"visitor",    u"Visitor")
    )

    user            = models.OneToOneField(User, verbose_name="user")
    # Names
    nickname        = models.CharField("nickname", max_length=32,
                        help_text="IRC nickname, or other kind of online handle.")
    real_name       = models.CharField("real name", max_length=64, blank=True,
                        help_text="The name you use in person.")
    preferred_name  = models.CharField("preferred name", max_length=4,
                        choices=PREFERRED_NAME_CHOICES, default=u"nick",
                        help_text="Which name you would prefer the site to use.")
    # LUG-related organizational info
    title           = models.CharField("title", max_length=64, blank=True,
                        help_text="Official LUG title, as officer or "
                                  "committee chair.")
    ordering        = models.PositiveIntegerField("ordering", default=0,
                        help_text="Relative order on the member directory, "
                                  "for LUG officers (higher numbers appear "
                                  "first, regular members should be 0).")
    role            = models.CharField("role", max_length=8,
                        choices=ROLE_CHOICES, default=u"visitor",
                        help_text="What your relationship is to NC State. "
                                  "(If you are not affiliated with NC State "
                                  "except through the LUG, choose Visitor.)")
    # Profile miscellanea
    is_protected    = models.BooleanField("profile protected?", default=False,
                        help_text="If this is set, only LUG members can view "
                                  "your profile.")
    biography       = models.TextField("biography", blank=True,
                        help_text="Anything you would like to say about "
                                  "yourself (in WikiCreole format).")

    def __unicode__(self):
        return u"%s (%s)" % self.names if self.has_both_names else self.name

    @staticmethod
    def make_username(nickname):
        return NON_USERNAME_CHARS.sub('', nickname.lower())

    # Name-related properties
    @property
    def name(self):
        if not self.real_name or self.preferred_name == u"nick":
            return self.nickname
        else:
            return self.real_name

    @property
    def alternate_name(self):
        if not self.real_name or self.preferred_name == u"nick":
            return self.real_name
        else:
            return self.nickname

    @property
    def names(self):
        if not self.real_name or self.preferred_name == u"nick":
            return (self.nickname, self.real_name)
        else:
            return (self.real_name, self.nickname)

    @property
    def has_both_names(self):
        return bool(self.real_name)

    # Bits!
    def all_bits(self):
        return self.bit_set.all()

    def bits_as_dict(self):
        return dict((bit.slug, bit.data) for bit in self.all_bits())

    # Authentication-related properties
    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email


class AccountRequest(models.Model):
    STATUS_CHOICES = (
        (u"pending",    u"Pending"),
        (u"deferred",   u"Deferred"),
        (u"approved",   u"Approved")
    )

    user            = models.OneToOneField(User, verbose_name="user")
    request_date    = models.DateTimeField("request date",
                        default=timezone.now,
                        help_text="The date the user made the request.")
    status          = models.CharField("status", max_length=8,
                        choices=STATUS_CHOICES, default=u"pending",
                        help_text="The current status of the request.")
    comments        = models.TextField("comments",
                        help_text="Comments explaining who you are.")

    @property
    def names(self):
        return self.user.get_profile().names

    @property
    def username(self):
        return self.user.username

    def approve(self):
        self.user.is_active = True
        self.user.save()
        self.status = u"approved"
        self.save()

    def destroy(self):
        self.user.get_profile().delete()
        self.user.delete()
        self.delete()


class BitType(models.Model):
    BIT_FORMATS = (
        (u"freetext",   u"Free Text"),
        (u"url",        u"URL"),
        (u"username",   u"Username")
    )

    slug            = models.SlugField("slug", max_length=16,
                        help_text="An internal identifier for bits of this "
                                  "type.")
    caption         = models.CharField("caption", max_length=32,
                        help_text="Text to caption the links with on users' "
                                  "profiles.")
    ordering        = models.PositiveIntegerField("ordering", db_index=True,
                        help_text="The position of links of this type "
                                  "relative to others. Lower numbers are "
                                  "sorted first.")
    format          = models.CharField("format", max_length=8,
                        choices=BIT_FORMATS, default=u"freetext",
                        help_text="The format that this bit takes. Used "
                                  "to validate things.")
    instructions    = models.CharField("instructions", max_length=128,
                        help_text="Instructions to display for entering bits "
                                  "of this type.")
    link_template   = models.CharField("link template", max_length=240,
                        blank=True,
                        help_text="A template for turning data of this type "
                                  "into a link. Include %s where it should "
                                  "be substituted in. Obviously useless for "
                                  "URLs.")

    class Meta:
        ordering    = ('ordering', 'caption')

    def __unicode__(self):
        return self.caption


username_validator = validators.RegexValidator("^[a-zA-Z0-9_.-`]+$",
                        u"The data must be a username (if this is "
                        "your actual username, contact leafstorm so he can "
                        "fix the regex).")

url_validator = validators.URLValidator()

class Bit(models.Model):
    owner           = models.ForeignKey(MemberProfile, verbose_name="owner")
    bit_type        = models.ForeignKey(BitType, verbose_name="type")
    data            = models.CharField("data", max_length=240)

    class Meta:
        ordering    = ('bit_type__ordering', 'bit_type__caption')

    def __unicode__(self):
        return u"%s: [%s]" % (self.bit_type.caption, self.data)

    def clean(self):
        format = self.bit_type.format
        if format == u"url":
            url_validator(self.data)
        elif format == u"username":
            username_validator(self.data)

    @property
    def caption(self):
        return self.bit_type.caption

    @property
    def slug(self):
        return self.bit_type.slug

    @property
    def data_url(self):
        bt = self.bit_type
        if bt.format == u"url":
            return self.data
        elif bt.link_template:
            template = bt.link_template
            format_idx, qmark_idx = template.find("%s"), template.find("?")
            if format_idx == -1:
                return template
            elif qmark_idx != -1 and format_idx > qmark_idx:
                return template % urllib.quote_plus(self.data)
            else:
                return template % urllib.quote(self.data)
        else:
            return None

    @property
    def data_html(self):
        url = self.data_url
        if url:
            return mark_safe('<a href="%s" rel="nofollow">%s</a>' %
                             (escape(url), escape(self.data)))
        else:
            return escape(self.data)

