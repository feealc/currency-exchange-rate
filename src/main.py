import requests
import datetime
from token_gmail import TOKEN_GMAIL
from custom.currency_handler import CurrencyHandler
from custom.gmail_handler import GmailHandler


def get_currency_rate(currency_from: str, currency_to: str):
    # bid - compra
    # ask - venda
    # varBid - variacao
    # pctChange - porcentagem de variacao
    # high - maximo
    # low - minimo

    cc = f'{currency_from}-{currency_to}'
    url = f'https://economia.awesomeapi.com.br/json/last/{cc}'
    response = requests.get(url, timeout=0.5)
    # print(response.json())
    cur_obj = CurrencyHandler(currency_from=currency_from, currency_to=currency_to, resp=response)
    return cur_obj


if __name__ == '__main__':
    currency_from_list = ['USD', 'EUR', 'GBP', 'CHF', 'BTC']
    body_email = ''
    for currency_from in currency_from_list[:]:
        currency_to = 'USD' if currency_from == 'BTC' else 'BRL'
        # print(currency_from + '-' + currency_to)
        cur = get_currency_rate(currency_from=currency_from, currency_to=currency_to)
        print(cur)
        body_email += f'<b>{cur.name} ({cur.cur_from}-{cur.cur_to})</b><br>{cur.bid}<br><br>'
    body_email += '<br>' + '<b>Gerado em:</b>' + '<br>' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    gmail = GmailHandler(email_owner='fernandobalcantara@gmail.com', password=TOKEN_GMAIL)
    now = datetime.datetime.now()
    gmail.set_subject(f'Valores cotação moedas para {now.strftime("%Y-%m-%d")}')
    gmail.set_to(same_as_owner=True)
    gmail.set_body(body_email)
    gmail.send()
