import argparse
import datetime
import requests
import logging
from token_gmail import TOKEN_GMAIL
from custom.currency_handler import CurrencyHandler
from custom.gmail_handler import GmailHandler
from custom.json_handler import *
from database.cer_db import CERDb
from logger.logger import logger


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
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email', action='store_true', help='Não realizar envio do e-mail com os resultados')
    args = parser.parse_args()

    logger.setLevel(logging.DEBUG)
    logger.info('### Início')

    obj = HandlerJsonProject()
    db = CERDb()
    db.prepare()
    # db.list_all_tables(debug=True)
    # db.delete_all()

    today = int(datetime.datetime.now().strftime('%Y%m%d'))

    body_email = ''
    for i in obj.get_currency_list():
        currency_from = i.get('from')
        currency_to = i.get('to')

        cur = None
        try:
            logger.info(f'Realizando consulta da cotação da moeda {currency_from}-{currency_to}')
            cur = get_currency_rate(currency_from=currency_from, currency_to=currency_to)
            logger.debug(f'Resultado da consulta: {cur}')
        except Exception as e:
            logger.exception(e)

        try:
            logger.debug(f'Inserindo cotação no banco de dados')
            db.insert_currency(date=today, name=cur.name_formatted, full_name=cur.name, value=cur.bid_float)
        except Exception as e:
            logger.exception(e)

        body_email += f'<b>{cur.name} ({cur.cur_from}-{cur.cur_to})</b><br>{cur.bid}<br><br>'
    body_email += '<br>' + '<b>Gerado em:</b>' + '<br>' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # db.select_all(debug=True)

    gmail = GmailHandler(email_owner='fernandobalcantara@gmail.com', password=TOKEN_GMAIL, flag_send=args.email)
    now = datetime.datetime.now()
    gmail.set_subject(f'Valores cotação moedas para {now.strftime("%Y-%m-%d")}')
    gmail.set_to(same_as_owner=True)
    gmail.set_body(body_email)
    gmail.send()

    logger.info('### Fim')
