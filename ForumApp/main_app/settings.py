import os

import peewee_async


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings = {
    "static_path": "/home/zpf/workarea/realForum/ForumApp/static",
    "static_prefix": "/static/",
    "template_path": "templates",
    "site_url": "http://127.0.0.1",
    "db": {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123',
        'port': 3306,
        'database': 'rfm'
    },
    "redis": {
        'host': '127.0.0.1'
    },
    "secret_key": "dp82cA9lEN5mk4 fGnsbuCqBkT7HARPj2",
    "jwt_expire": 7 * 24 * 3600,
    "MEDIA_ROOT": os.path.join(BASEDIR, "media")
}

database = peewee_async.MySQLDatabase(**settings["db"])
