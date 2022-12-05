from .currency_handler import CurrencyHandler
from .json_handler import HandlerJsonCERHistory


class CurrencyHistoryHandler:
    def __init__(self):
        self.__json = HandlerJsonCERHistory()
        self.history: list[HistoryRecord] = []
        self.__parse_history()

    def __parse_history(self):
        self.history = []
        hist = self.__json.get_file()['history']
        for h in hist:
            hr = HistoryRecord(record=h)
            # print(hr)
            self.history.append(hr)

    def dump(self):
        for h in self.history:
            print(h)

    def add_today_cer(self, today: str, cur: CurrencyHandler):
        # print('add_today_cer() - inicio')
        # print(f'date_exist [{self.date_exist(date=today)}]')
        if self.date_exist(date=today):
            for h in self.history:
                if h.date == today:
                    h.add_cer(cur=cur)
        else:
            hr = HistoryRecord(today=today)
            hr.add_cer(cur=cur)
            self.history.append(hr)

    def date_exist(self, date: str) -> bool:
        for h in self.history:
            if h.date == date:
                return True
        return False


class HistoryRecord:
    def __init__(self, record: dict = None, today: str = None):
        self.date: str = ''
        self.info_list: list[(str, float)] = []

        if record is not None:
            self.__parse_record(record=record)

        if today is not None:
            self.date = today

    def __str__(self):
        aux = f'{self.date} > '
        for name, value in self.info_list:
            aux += f'{name} : {value:6} | '
        return aux[:-3]

    def __parse_record(self, record: dict):
        self.date = record.get('date')

        self.info_list = []
        for info in record.get('info'):
            tup = (info.get('name'), info.get('value'))
            self.info_list.append(tup)

    def add_cer(self, cur: CurrencyHandler):
        self.info_list.append(cur.to_tuple())
