from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms

class PlekReserveringForm(forms.Form):
    plaats = forms.CharField(
        max_length=40,
        required=True
    )

    datum_begin = forms.DateField(
        required=True
    )

    datum_eind = forms.DateField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(PlekReserveringForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("plaats"),
            Field("datum_begin", css_class="datepicker"),
            Field("datum_eind", css_class="datepicker"),

            Submit("submit", "Submit", css_class="btn-primary btn-block")
        )