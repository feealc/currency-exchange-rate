import sqlite3
import os
from pathlib import Path


class CERDb:
    def __init__(self):
        self.db_name = os.path.join(Path(__file__).parent.parent.parent, 'cer_history.db')
        self.__conn = None
        self.__cursor = None
        self.__tb_history = 'tb_cer_history'

    def __connect(self):
        self.__conn = sqlite3.connect(self.db_name)
        self.__cursor = self.__conn.cursor()

    def __commit(self):
        if self.__conn:
            self.__conn.commit()

    def __close_conn(self):
        if self.__conn:
            self.__conn.close()

    def __table_exist(self, table_name: str):
        self.__connect()
        self.__cursor.execute(f"""
        SELECT name FROM sqlite_master WHERE type='table' and name='{table_name}'
        """)
        return False if self.__cursor.fetchone() is None else True

    def __create_table_history(self):
        print(f'Criando tabela {self.__tb_history}')
        self.__connect()
        self.__cursor.execute(f"""
        CREATE TABLE {self.__tb_history} (
                date INTEGER NOT NULL,
                name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                value REAL NOT NULL,
                PRIMARY KEY (date, name)
        );
        """)
        self.__commit()
        self.__close_conn()

    def prepare(self):
        self.__connect()
        self.__close_conn()
        #
        if not self.__table_exist(table_name=self.__tb_history):
            self.__create_table_history()

    def list_all_tables(self, debug: bool = False):
        self.__connect()
        self.__cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        """)
        all_tables = self.__cursor.fetchall()
        if debug:
            print('Tabelas:')
            for tabela in all_tables:
                print('> [%s]' % tabela)
        self.__close_conn()
        return all_tables

    def list_columns_from_table(self, table_name: str, debug: bool = False):
        self.__connect()
        self.__cursor.execute('PRAGMA table_info({})'.format(table_name))
        cols = [tupla[1] for tupla in self.__cursor.fetchall()]
        if debug:
            print(f'Colunas tabela {table_name}: {cols}')
        self.__close_conn()
        return cols

    """
    ===============================================================================================
    INSERT
    ===============================================================================================
    """
    def insert_currency(self, date: int, name: str, full_name: str, value: float):
        self.__connect()
        self.__cursor.execute(f"""
        INSERT INTO {self.__tb_history}
        VALUES (?,?,?,?)
        """, (date, name, full_name, value))
        self.__commit()
        self.__close_conn()

    """
    ===============================================================================================
    SELECT
    ===============================================================================================
    """
    def select_all(self, debug: bool = False):
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.__tb_history} ORDER BY date, name;
        """)
        lines = self.__cursor.fetchall()
        if debug:
            for line in lines:
                print(line)
        self.__close_conn()
        return lines

    """
    ===============================================================================================
    UPDATE
    ===============================================================================================
    """

    """
    ===============================================================================================
    DELETE
    ===============================================================================================
    """
    def delete_all(self):
        self.__connect()
        self.__cursor.execute(f"""
        DELETE FROM {self.__tb_history};
        """)
        self.__commit()
        self.__close_conn()
