from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Div
# from crispy_forms.bootstrap import FormActions
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):

    # username and password provided by UserCreationForm
    email = forms.EmailField()
    first_name = forms.CharField
    last_name = forms.CharField

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Account details',
                Field('username'), Field('password1'), Field('password2'),
            ),
            Fieldset(
                'Extra Information',
                Field('first_name'), Field('last_name'), Field('email')
            ),
            Div(
                Div(
                    Submit('register', 'Register'),
                    css_class='col-lg-offset-2 col-lg-10'
                ),
                css_class='form-group'
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'There is already a user with that email.')
        return email
