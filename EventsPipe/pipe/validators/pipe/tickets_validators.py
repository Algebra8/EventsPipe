from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_cost(value):
    if type(value) != float:
        raise ValidationError(
            _('%(value)s is not a float'),
            params={'value': value},
        )

def validate_event_id(value):
    try:
        if not repr(value) == 'Event':
            raise ValidationError(
                _('%(value)s is not an Event object'),
                params={'value': value},
            )
    except ValueError:
        raise ValidationError(
            _('%(value)s is not an Event object'),
            params={'value': value},
        )
