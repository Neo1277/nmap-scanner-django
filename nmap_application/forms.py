from django import forms
from .models import ScannerHistory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset,ButtonHolder
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

# strip means to remove whitespace from the beginning and the end before storing the column
class ScannerForm(forms.Form):

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = ScannerHistory
        fields = [
            'target',
            'type'
        ]

    target = forms.CharField(
        required=True,
        max_length=500,
        min_length=3,
        strip=True
    )

    # Choices for field type
    QUICK = 'QS'
    FULL = 'FS'
    type = forms.ChoiceField(
        choices = (
            (QUICK, "Quick scan"),
            (FULL, "Full scan")
        ),
        widget = forms.RadioSelect,
        initial = 'QS',
    )

# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
# https://gist.github.com/maraujop/1838193