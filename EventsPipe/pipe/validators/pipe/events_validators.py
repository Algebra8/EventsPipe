from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_id(value):
    if type(value) != int:
        raise ValidationError(
            _('%(value)s is not an integer'),
            params={'value': value},
        )

def validate_startdate(value):
    if type(value) == str:
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')

        except ValueError:
            raise ValidationError(
                _('%(value)s is incorrect data format, ' \
                  + 'should be YYYY-MM-DD'),
                params={'value': value},
            )
    else:
        return
