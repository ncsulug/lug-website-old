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
        self.preview_content = None
        super(EditForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'content' in cleaned_data and cleaned_data['content'].strip():
            self.preview_content = cleaned_data['content']
        return cleaned_data

    def save(self, *args, **kwargs):
        if not self.page.pk:
            self.page.save()
            self.instance.page = self.page
        return super(EditForm, self).save(*args, **kwargs)
