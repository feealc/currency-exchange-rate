import requests
import datetime
from token_gmail import TOKEN_GMAIL
from custom.currency_handler import CurrencyHandler
from custom.currency_history_handler import CurrencyHistoryHandler
from custom.gmail_handler import GmailHandler
from custom.json_handler import *


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
    body_email = ''

    today = datetime.datetime.now().strftime('%Y%m%d')
    # today = '20221122'
    # print(today)
    cur_hist = CurrencyHistoryHandler()
    cur_hist.dump()

    obj = HandlerJsonProject()
    for i in obj.get_currency_list():
        currency_from = i.get('from')
        currency_to = i.get('to')
        # print(currency_from + '-' + currency_to)
        cur = get_currency_rate(currency_from=currency_from, currency_to=currency_to)
        cur_hist.add_today_cer(today=today, cur=cur)
        print(cur)
        body_email += f'<b>{cur.name} ({cur.cur_from}-{cur.cur_to})</b><br>{cur.bid}<br><br>'
    body_email += '<br>' + '<b>Gerado em:</b>' + '<br>' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur_hist.dump()

    # gmail = GmailHandler(email_owner='fernandobalcantara@gmail.com', password=TOKEN_GMAIL)
    # now = datetime.datetime.now()
    # gmail.set_subject(f'Valores cotação moedas para {now.strftime("%Y-%m-%d")}')
    # gmail.set_to(same_as_owner=True)
    # gmail.set_body(body_email)
    # gmail.send()
