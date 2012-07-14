# -*- coding: utf-8 -*-
from .models import MemberProfile, Bit
from django import forms
from django.forms.models import ModelForm, inlineformset_factory

class ProfileEditForm(ModelForm):
    class Meta:
        model = MemberProfile
        fields = ('nickname', 'real_name', 'preferred_name', 'role')


BitFormSet = inlineformset_factory(MemberProfile, Bit, fk_name="owner", extra=3)
