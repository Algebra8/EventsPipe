from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_cost(value):
    """
    Ticket model validator for ticket_cost
    """
    if type(value) != float:
        raise ValidationError(
            _('%(value)s is not a float'),
            params={'value': value},
        )
