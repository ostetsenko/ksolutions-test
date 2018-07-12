import json
import logging.handlers
from hashlib import sha256
import requests

from flask import render_template, request, redirect, flash

from app import app, babel
from app.constants import ADDITION_PROPERTIES, CURRENCY_CODES
from app.config import LANGUAGES
from flask_babel import lazy_gettext as _

from app.forms import StartPaymentForm

logger = logging.getLogger(__name__)


@babel.localeselector
def get_locale():
    prefered_language = request.accept_languages.best_match(LANGUAGES.keys())
    logger.debug('Main interface language: %s' % prefered_language)
    return prefered_language


def get_sign(required_fields):
    """
    :param required_fields: dict of required fields for request
    :return: HEX-sign
    """
    keys = required_fields.keys()
    sorted_keys = sorted(keys)
    prepared_sign = ":".join(str(required_fields[field]) for field in sorted_keys)
    prepared_sign += ADDITION_PROPERTIES.get('SECRET_KEY_PAY', '')
    code = sha256(prepared_sign.encode()).hexdigest()
    return code


def pay_request(amount=0, currency='eur', description='Not exists'):
    """
    :param amount: float
    :param currency: str
    :param description: str
    :return:
    """
    logger.info('PAY request started: %.2f %s %s' % (amount, currency, description))
    SHOP_ORDER_ID = 101
    URLs = {
        'en': 'https://pay.piastrix.com/en/pay',
        'ru': 'https://pay.piastrix.com/ru/pay'}
    language = request.accept_languages.best_match(URLs.keys())
    form = {
        'amount': amount,
        'currency': CURRENCY_CODES.get(currency),
        'shop_id': ADDITION_PROPERTIES.get('SHOP_ID', -1),
        'shop_order_id': SHOP_ORDER_ID}
    form['sign'] = get_sign(form)
    form['description'] = description

    context = {
        'url': URLs.get(language),
        'method': 'post',
        'form': form}
    logger.info('PAY request send form to apply')
    print(type(render_template('index.html', payment='pay', **context)))
    return render_template('index.html', payment='pay', **context)


def bill_request(amount=0, currency='usd', description='Not exists', payer_currency=None):
    logger.info('BILL request started: %.2f %s %s' % (amount, currency, description))
    SHOP_ORDER_ID = 101
    url = 'https://core.piastrix.com/bill/create'
    headers = {'Content-type': 'application/json',
               'Content-Encoding': 'utf-8'}
    data = {
        'shop_amount': amount,
        'shop_currency': CURRENCY_CODES.get(currency),
        'shop_id': ADDITION_PROPERTIES.get('SHOP_ID', -1),
        'shop_order_id': SHOP_ORDER_ID,
        'payer_currency': CURRENCY_CODES.get(payer_currency or currency)}
    data['sign'] = get_sign(data)
    try:
        logger.info('Post request to BILL(%s)' % (url,))
        response = requests.post(url, data=json.dumps(data), headers=headers)
    except:
        logger.info('BILL site not found.')
        return render_template('error.html', messages={_('No answer'): _('Site %s is not responding.') % url})

    content = json.loads(response.content)

    if content['result']:
        logger.info('Post request to BILL(%s): Success' % (url,))
        return redirect(content['data']['url'])

    errors = {
        'service': 'bill',
        'code': content['error_code'],
        'message': content['message'],
    }
    logger.info('Post request to BILL(%s): Error. Code: %d. Message:%s' % (url, errors['code'], errors['message'],))
    return render_template('error.html', messages=errors)


def invoice_request(amount=0, currency='rub', description='Not exists'):
    logger.info('INVOICE request started: %.2f %s %s' % (amount, currency, description))
    SHOP_ORDER_ID = 123456
    url = 'https://core.piastrix.com/invoice/create'
    headers = {'Content-type': 'application/json',
               'Content-Encoding': 'utf-8'}
    data = {
        'amount': amount,
        'currency': CURRENCY_CODES.get(currency),
        'shop_id': ADDITION_PROPERTIES.get('SHOP_ID', -1),
        'shop_order_id': SHOP_ORDER_ID,
        'payway': ADDITION_PROPERTIES.get('PAYWAY', 'unknown')}
    data['sign'] = get_sign(data)
    try:
        logger.info('Post request to INVOICE(%s)' % (url,))
        response = requests.post(url, data=json.dumps(data), headers=headers)
    except:
        logger.info('INVOICE site not found.')
        return render_template('error.html', messages={_('No answer'): _('Site %s is not responding.') % url})

    content = json.loads(response.content)

    if content['result']:
        context = {
            'url': content['data']['url'],
            'method': content['data']['method'],
            'form': content['data']['data']}
        logger.info('Post request to INVOICE(%s): Success' % (url,))
        logger.info('INVOICE request send form to apply')
        return render_template('index.html', payment='invoice', **context)
    errors = {
        'service': 'invoice',
        'code': content['error_code'],
        'message': content['message'],
    }
    logger.info('Post request to INVOICE(%s): Error. Code: %d. Message:%s' % (url, errors['code'], errors['message'],))
    return render_template('error.html', messages=errors)


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info('Getting index page.')
    form = StartPaymentForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.currency.data == 'eur':
            return pay_request(form.amount.data, form.currency.data, form.description.data)
        elif form.currency.data == 'usd':
            return bill_request(form.amount.data, form.currency.data, form.description.data)
        elif form.currency.data == 'rub':
            return invoice_request(form.amount.data, form.currency.data, form.description.data)
        else:
            logger.error('Not allowed currency')
            return render_template('error.html',
                                   messages={_('curruncy'): _("%s - unknown currency") % form.currency.data})
    return render_template('index.html', form=form)
