from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms import validators, FloatField

from app.constants import CURRENCY_CODES


class StartPaymentForm(FlaskForm):
    amount = FloatField(_('Amount'), validators=[validators.required(_("Field is required. Field must be a number."))])
    currency = SelectField(_('Currency'),
                           coerce=str,
                           choices=[(str(code), str(code).upper()) for code in sorted(CURRENCY_CODES.keys())],
                           default=0)
    description = TextAreaField(_('Product description'), validators=[validators.required()])

