from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms


class PlekReserveringForm(forms.Form):
    plek = forms.CharField(
        max_length=40,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(PlekReserveringForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("plek"),

            Submit("submit", "Submit", css_class="btn-primary btn-block")
        )
