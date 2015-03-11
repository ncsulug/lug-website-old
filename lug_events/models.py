from django.core.exceptions import ValidationError
from django.db import models

def ncsu_semester(date):
    """
    An algorithm for estimating NC State University semester start dates.

    * Spring is January 1-May 14.
    * Summer is May 15-August 14.
    * Fall is August 15-December 31.
    """
    if date.month < 5:
        return "Spring"
    elif date.month == 5 and date.day < 15:
        return "Spring"
    elif date.month < 8:
        return "Summer"
    elif date.month == 8 and date.month < 15:
        return "Summer"
    else:
        return "Fall"


class EventKind(models.Model):
    singular        = models.CharField(max_length=32,
                        help_text="What we call this kind of event, title case. "
                                  "Examples: Hack Day, Technical Meeting, "
                                  "Social Dinner, Business Meeting")
    plural          = models.CharField(max_length=32,
                        help_text="Pluralize the name above.")
    description     = models.CharField(max_length=128,
                        help_text="A tooltip description for this event kind. "
                                  "This should be a noun phrase capitalized "
                                  "and punctuated as a sentence.")

    class Meta:
        ordering = ['plural']

    def __unicode__(self):
        return self.plural


class Event(models.Model):
    name            = models.CharField(max_length=64,
                        help_text="The event's name, to go on the calendar. "
                                  "Repeating names is OK.")
    kind            = models.ForeignKey(EventKind, null=False)
    start_time      = models.DateTimeField()
    end_time        = models.DateTimeField()

    speaker         = models.CharField(max_length=48, blank=True,
                        help_text="The name of the speaker or sponsor, "
                                  "if applicable. "
                                  "Examples: \"Matthew Frazier\", "
                                  "\"Jim Whitehurst of Red Hat\"")
    location        = models.CharField(max_length=64,
                        help_text="The event's location. Examples: "
                                  "\"Engineering Building II 1227\", "
                                  "\"2426 Hillsborough St\", "
                                  "\"Location TBD\"")
    pitch           = models.TextField(blank=True,
                        help_text="A quick paragraph describing the event and "
                                  "encouraging people to attend. "
                                  "For full details, use the URL below. "
                                  "Plain text.")

    custom_url      = models.URLField("Custom URL", blank=True,
                        help_text="A custom URL for the event, to use instead "
                                  "of a wiki page.")

    advisory        = models.CharField(max_length=32, blank=True,
                        help_text="Some sort of notice that needs to be "
                                  "advertised for the event. It will be displayed "
                                  "prominently and with a sense of urgency. "
                                  "Example: Cancelled due to inclement weather")
    on_website      = models.BooleanField("display on Web site", default=True,
                        help_text="Whether to display this event in the events "
                                  "lineup on the homepage and the history page.")
    on_billboard    = models.BooleanField("display on Billboard", default=True,
                        help_text="Whether to display this event on the "
                                  "Billboard slides.")

    class Meta:
        get_latest_by = 'start_time'
        ordering = ['-start_time']

    def __unicode__(self):
        return self.name

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Events must end after they start.")

    @property
    def semester(self):
        return ncsu_semester(self.start_time) + self.start_time.strftime(" %Y")

    @property
    def has_link(self):
        return bool(self.custom_url)

    def get_absolute_url(self):
        if self.custom_url:
            return self.custom_url
        else:
            return '/events/' # FIXME

