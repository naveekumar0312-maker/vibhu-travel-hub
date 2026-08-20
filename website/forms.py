# pyrefly: ignore [missing-import]
from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):

    class Meta:

        model = Enquiry

        fields = [
            'name',
            'email',
            'phone',
            'service',
            'message'
        ]