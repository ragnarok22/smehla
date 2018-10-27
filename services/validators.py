from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_born_date(born_date):
    if born_date.year >= date.today().year:
        raise ValidationError(
            _('%(born_date)s is not a correct born date'),
            params={'born_date': born_date}
        )
