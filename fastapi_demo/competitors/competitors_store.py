from rethinkdb import r
from rethinkdb.errors import ReqlOpFailedError, ReqlDriverError
from pydantic.networks import IPv4Address


class CompetitorsStore:

    def __init__(self, conn_string: str = "localhost", port: int = 32775):
        self._conn_string = conn_string
        self._port = port
        self._db_up = True
        try:
            conn = r.connect(conn_string, port)
            r.db('test').table_create('competitors').run(conn) # setup db
        except ReqlDriverError as err:
            print("Could not connect to DB")
            self._db_up = False
        except ReqlOpFailedError as ex:
            print("DB exists")

    def get_competitors(self):
        try:
            conn = r.connect(self._conn_string, self._port)
            competitors = []
            cursor = r.table("competitors").run(conn)
            for document in cursor:
                competitors.append(document)
            return competitors
        except ReqlDriverError as err:
            print("Could not connect to DB")
        return []

    def delete_competitor(self, id: str):
        try:
            conn = r.connect(self._conn_string, self._port)
            return r.table("competitors").get(id).delete().run(conn)
        except ReqlDriverError as err:
            print("Could not connect to DB")
        return []

    def store_competitor(self, competitor):
        try:
            conn = r.connect(self._conn_string, self._port)
            competitor["ip_addr"] = str(competitor["ip_addr"])
            return r.table("competitors").insert(competitor).run(conn)
        except ReqlDriverError as err:
            print("Could not connect to DB")
        return []
