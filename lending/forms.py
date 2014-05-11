from __future__ import absolute_import

# import datetime

from django import forms
from django.core.urlresolvers import reverse
# from django.core.exceptions import ValidationError
# from django.utils.timezone import utc

from crispy_forms.layout import Layout, Submit, Fieldset, Field, Div

from toolhub.forms import CrispyFormMixin
from . import models


class TransactionForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        fields = ('purpose',)
        model = models.Transaction

    def __init__(self, hub_slug, usertool_id, *args, **kwargs):
        # hub_slug = kwargs.pop('hub_slug', None)
        # usertool_id = kwargs.pop('usertool_id', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse(
            'lending:new_transaction',
            kwargs={'hub_slug': hub_slug, 'usertool_id': usertool_id})
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        # TODO, display information about the usertool in form
        self.helper.layout = Layout(
            Fieldset(
                'Lending Request Details',
                Field('purpose')
            ),
            Div(
                Div(
                    Submit('request', 'Request Tool'),
                    css_class='col-md-offset-3 col-md-9'
                ),
                css_class='form-group'
            ))
