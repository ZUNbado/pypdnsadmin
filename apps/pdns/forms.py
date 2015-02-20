from django import forms
from .models import Domain, Record, DomainTemplate

from django.contrib.admin import widgets

class RecordInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['name'].widget.attrs['readonly'] = 'True'
            self.fields['type'].widget = widgets.AdminTextInputWidget()
            self.fields['type'].widget.attrs['readonly'] = 'True'

    class Meta:
        model = Record
        fields = '__all__'

class DomainCreateForm(forms.ModelForm):
    template = forms.ModelChoiceField(queryset=DomainTemplate.objects.all(), required = False)
    def __init__(self, *args, **kwargs):
        super(DomainCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Domain
        fields = '__all__'
