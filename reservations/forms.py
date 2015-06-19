from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django import forms


class EmailReservationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EmailReservationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("email"),

            FormActions(
                Submit('post', 'Post', css_class=" btn-primary btn-block"),
            )
        )

    email = forms.CharField(
        widget=forms.EmailInput,
        required=True,
    )


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field("email"),
            Field("first_name"),
            Field("last_name"),
            Field("street"),
            Field("house_number"),
            Field("town"),
            Field("bank_number"),

            FormActions(
                Submit('post', 'Post', css_class=" btn-primary btn-block"),
            )
        )

    email = forms.CharField(
        widget=forms.EmailInput,
        required=True,
    )

    first_name = forms.CharField(
        required=True
    )

    street = forms.CharField(
        required=True
    )

    house_number = forms.CharField(
        required=True
    )

    town = forms.CharField(
        required=True
    )

    bank_number = forms.CharField(
        required=True,
    )

    last_name = forms.CharField(
        required=True
    )
