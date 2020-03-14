from fastapi import HTTPException
from rethinkdb import r
from rethinkdb.errors import ReqlOpFailedError, ReqlDriverError
from fastapi.logger import logger
r.set_loop_type("asyncio")

from fastapi_demo.competitors.competitor import CompetitorModel

class CompetitorsStore:

    def __init__(self, conn_string: str, port: int):
        self._conn_string = conn_string
        self._port = port
        self._db_is_setup = False
        self._conn = None                               # Connection not setup

    async def setup_db(self):
        try:
            self._conn = await r.connect(self._conn_string, self._port)
            if "competition" not in await r.db_list().run(self._conn):                  # setup db and tables
                await r.db_create("competition").run(self._conn)
                await r.db('competition').table_create('competitors').run(self._conn)
        except ReqlDriverError as err:
            logger.warning(f"Could not connect to DB: {err}")
        except ReqlOpFailedError as ex:
            logger.warning(f"DB creation error: {ex}")
        self._db_is_setup = True

    async def close_connection(self):
        await self._conn.close()

    async def get_competitors(self):
        try:
            competitors = []
            cursor = await r.db('competition').table("competitors").run(self._conn)
            async for document in cursor:
                competitors.append(document)
            return competitors
        except ReqlOpFailedError as err:
            logger.warning(f"DB Error: {err}")
        return []

    async def delete_competitor(self, id: str):
        try:
            return await r.db('competition').table("competitors").get(id).delete().run(self._conn)
        except ReqlOpFailedError as err:
            logger.warning(f"DB Error: {err}")
        return []

    async def register_competitor(self, registration):
        as_dict = registration.dict()
        as_dict["ip_addr"] = str(as_dict["ip_addr"])
        competitor = CompetitorModel(**as_dict, points=0, challenge_level=1)
        try:
            result = await r.db('competition').table("competitors").insert(competitor.dict()).run(self._conn)
            if result["errors"] != 0:
                logger.error(f"DB request error: {result['first_error']}")
                raise HTTPException(status_code=500,
                                    detail=f"could not insert record into DB: Competitor({competitor})")
            return result
        except ReqlOpFailedError as err:
            logger.error(f"DB Error: {err}")
            raise HTTPException(status_code=500,
                                detail=f"could not insert record into DB: Competitor({competitor})")

