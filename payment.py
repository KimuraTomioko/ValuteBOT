import yookassa
from yookassa import Payment
import uuid

yookassa.Configuration.account_id = '373694'
yookassa.Configuration.secret_key = 'test_EUwHYFVDaiNlYiZDeSH37QMAcbU-xS0FNZGBQIqoWVo'


def create(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            'value': amount,
            'currency': "RUB"
        },
        'paymnet_method_data': {
            'type': 'bank_card'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': 'https://t.me/Call_Of_Duty_Gold_Shop_bot'
        },
        'capture': True,
        'metadata': {
            'chat_id': chat_id
        },
        'description': 'Описание товара....'
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id


def check(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return payment.metadata
    else:
        return False