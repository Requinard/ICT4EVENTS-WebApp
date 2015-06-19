from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms


class BarcodeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BarcodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("barcode"),

            FormActions(
                Submit('post', 'Scan code', css_class=" btn-primary btn-block"),
            )
        )

    barcode = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'autofocus': 'true'})
    )
