# -*- coding: utf-8 -*-

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class ChloroformHelper(FormHelper):
    layout = Layout(
        Field('message'),
        Field('nom'),
        Field('prenom'),
    )

    def __init__(self, form):
        # Discard the form
        super(ChloroformHelper, self).__init__()
