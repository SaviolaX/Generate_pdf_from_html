from django import forms

from .models import Document


class DateInput(forms.DateInput):
    """
    Set a date input field in html page
    type=text -> type=date
    """
    input_type = 'date'


class DocumentCreateForm(forms.ModelForm):
    """Form for creating and updating instance object"""
    class Meta:
        model = Document
        fields = ('first_name', 'last_name', 'company', 'car',
                  'renting_date_from', 'renting_date_to')

        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'company': forms.TextInput(),
            'renting_date_from': DateInput,
            'renting_date_to': DateInput
        }
