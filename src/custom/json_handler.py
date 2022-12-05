import json


class HandlerJson:
    def __init__(self, file_name):
        self._file_json: dict = None
        self._file_name = file_name

        self.__load_file()

    def __load_file(self):
        with open(self._file_name, 'r', encoding='utf-8') as f:
            self._file_json = json.load(f)

    def dump_json(self):
        print(json.dumps(self._file_json, indent=4, ensure_ascii=False))

    def get_file(self):
        return self._file_json

    def reload_file(self):
        self.__load_file()


class HandlerJsonProject(HandlerJson):
    def __init__(self):
        super(HandlerJsonProject, self).__init__(file_name='json/project.json')

    def get_currency_list(self) -> list[dict]:
        return self._file_json.get('currency_list')


class HandlerJsonCERHistory(HandlerJson):
    def __init__(self):
        super(HandlerJsonCERHistory, self).__init__(file_name='json/cer_history.json')
