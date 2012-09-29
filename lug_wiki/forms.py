from .models import Page, Revision
from django import forms
from django.forms.models import ModelForm

class EditForm(ModelForm):
    class Meta:
        model = Revision
        fields = ('content', 'change_note')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'span7'})
        }

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        super(EditForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.page.pk:
            self.page.save()
            self.instance.page = self.page
        return super(EditForm, self).save(*args, **kwargs)
