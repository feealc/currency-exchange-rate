import requests


class CurrencyHandler:
    def __init__(self, currency_from: str, currency_to: str, resp: requests.Response):
        self.__currency_from = currency_from
        self.__currency_to = currency_to
        self.__response = resp

        self.__currency_name = None
        self.__currency_value = None

        self.__parse_resp()

    @property
    def name(self):
        return self.__currency_name

    @property
    def bid(self):
        return self.__currency_value

    @property
    def cur_from(self):
        return self.__currency_from

    @property
    def cur_to(self):
        return self.__currency_to

    def __str__(self):
        return self.get_desc()

    def __parse_resp(self):
        st = self.__response.status_code
        if st != 200:
            raise Exception(f'Erro na consulta da moeda {self.__currency_from} para {self.__currency_to} - status code {st}')
        resp_json: dict = self.__response.json()
        resp_json_cur: dict = resp_json.get(f'{self.__currency_from}{self.__currency_to}')
        self.__currency_name = resp_json_cur.get('name', '')
        self.__currency_value = resp_json_cur.get('bid', 0.0)
        # print(json.dumps(resp_json, indent=4, ensure_ascii=False))

    def get_desc(self):
        return f'{self.__currency_from}-{self.__currency_to} > {self.__currency_value} ({self.__currency_name})'
