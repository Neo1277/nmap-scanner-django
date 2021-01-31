from django import forms
from .models import ScannerHistory

# strip means to remove whitespace from the beginning and the end before storing the column
class ScannerForm(forms.Form):

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = ScannerHistory
        fields = ['target']

    target = forms.CharField(
        required=True,
        max_length=500,
        min_length=3,
        strip=True
    )


# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
