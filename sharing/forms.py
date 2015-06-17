from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms

class BerichtForm(forms.Form):
    title = forms.CharField(max_length=80)
    bericht = forms.CharField(
        widget=forms.TextInput,
        required=True,
        max_length=255
    )
    bestand = forms.FileInput()

    def __init__(self, *args, **kwargs):
        super(BerichtForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("title"),
            Field("bericht"),
            Field("bestand"),

            FormActions(
                Submit('post', 'Post', css_class=" btn-primary btn-block"),
            )
        )
class CommentForm(forms.Form):
    bericht = forms.CharField(
        required=True,
        max_length=255
    )

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("bericht"),

            FormActions(
                Submit('post', 'Post', css_class=" btn-primary btn-block"),
            )
        )




