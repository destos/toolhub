from crispy_forms.layout import Layout, Fieldset, Submit, Field, Div
from django import forms
from django.utils.translation import ugettext_lazy as _

from toolhub.forms import CrispyFormMixin
from .models import Tool, UserTool


class CreateUserToolForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        fields = ('callsign', 'portability', 'tool_type')
        model = UserTool

    def __init__(self, *args, **kwargs):
        super(CreateUserToolForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'tools:create'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(
                _('Add a tool'),
                Field('callsign'), Field('portability'), Field('tool_type')
            ),
            Div(
                Div(
                    Submit('create', _('add tool')),
                    css_class='col-md-offset-2 col-md-10'
                ),
                css_class='form-group'
            ))


class SuggestToolForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        fields = ('name', 'description', 'model_number', 'parent', 'value',
                  'weight')
        model = Tool

    def __init__(self, *args, **kwargs):
        super(SuggestToolForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'tools:suggest'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(
                _('Required Information'),
                Field('name', 'description')
            ),
            Fieldset(
                _('Tool Details'),
                Field('model_number'), Field('value'), Field('weight'),
                Field('parent')
            ),
            Div(
                Div(
                    Submit('create', _('suggest tool')),
                    css_class='col-md-offset-2 col-md-10'
                ),
                css_class='form-group'
            ))
