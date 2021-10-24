from django import forms

from .models import *


class AddPostForm(forms.ModelForm):
    # fio = forms.CharField()
    # email = forms.EmailField()
    # telephone
    # character
    time = forms.DateTimeField(widget=forms.NumberInput(attrs={'type': 'datetime-local'}))
    name_industry = forms.ModelChoiceField(queryset=Industry.objects.all())
    # city
    street = forms.ModelChoiceField(queryset=Street.objects.all())
    # house_number
    # comment

    class Meta:
        model = AddPollution
        fields = ['fio', 'email', 'telephone', 'character', 'time',
                  'name_industry', 'city', 'street', 'house_number', 'comment', ]

        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'telephone': forms.NumberInput(),
            'character': forms.TextInput(attrs={'class': 'form-input'}),
            # 'time': forms.DateTimeInput(),
            # 'name_industry': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            # 'street': forms.Select(choices=Street.objects.all()),
            'house_number': forms.TextInput(attrs={'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def clean_user_name(self):
        fio = self.cleaned_data.get('fio')
        # if len(fio) > 10:
        #     raise ValidationError('больше 10')

        return fio
