import aiomysql
from tornado import web, ioloop, gen


class IndexHandler(web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self):
        sid = name = email = address = msg = ""
        async with aiomysql.create_pool(**self.db) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT id, name, email, address, msg FROM msg")
                    try:
                        sid, name, email, address, msg = cur.fetchone().result()
                    except TypeError:
                        pass
        await self.render("message.html", sid=sid, name=name, email=email, address=address, msg=msg)

    async def post(self):
        sid = self.get_body_argument("sid")
        name = self.get_body_argument("name")
        email = self.get_body_argument("email")
        address = self.get_body_argument("address")
        msg = self.get_body_argument("message")
        async with aiomysql.create_pool(**self.db) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    if sid == "":
                        await cur.execute(
                            f"INSERT INTO msg(name, email, address, msg) "
                            f"VALUES('{name}', '{email}', '{address}', '{msg}')"
                        )
                    else:
                        await cur.execute(
                            f"UPDATE msg SET "
                            f"name='{name}', email='{email}', address='{address}', msg='{msg}' WHERE id='{sid}'"
                        )
                await conn.commit()


settings = {
    "static_path": "/home/zpf/workarea/realForum/MsgBoard/static",
    "static_prefix": "/static/",
    "template_path": "templates",
    "db": {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123',
        'port': 3306,
        'db': 'rfm'
    }
}

if __name__ == "__main__":
    app = web.Application([
        web.URLSpec("/", IndexHandler, {"db": settings["db"]}, name="index")
    ], debug=True, **settings)
    app.listen(8080)
    ioloop.IOLoop.current().start()
