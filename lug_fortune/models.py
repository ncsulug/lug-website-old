from django.db import models


# Create your models here.
class Fortune(models.Model):
    value = models.CharField("fortune", max_length=240,
                             help_text=u"The fortune text!")
    priority = models.BooleanField("priority", default=False,
                               help_text=u"If true, this fortune always appears.")
    
    class Meta:
        verbose_name = 'fortune'
        verbose_name_plural = 'fortunes'

    def __unicode__(self):
        return self.value


