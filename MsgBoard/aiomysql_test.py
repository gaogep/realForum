import asyncio
import aiomysql


async def test():
    sid = 10
    name = "testname"
    email = "1@test.com"
    address = "testwuhan"
    msg = "testmsg"
    async with aiomysql.create_pool(host='127.0.0.1', port=3306, user='root', password='123', db='rfm') as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"UPDATE msg SET name='{name}', email='{email}', address='{address}', msg='{msg}' WHERE id='{sid}'"
                )
                # await cur.execute(
                #     f"INSERT INTO msg(name, email, address, msg) VALUES('{name}', '{email}', '{address}', '{msg}')"
                # )
                # sid, name, email, address, msg = cur.fetchone().result()
                # print(sid, name, email, address, msg)
                await conn.commit()
    pool.close()
    await pool.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
