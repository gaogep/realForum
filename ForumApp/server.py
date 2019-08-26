from tornado import web, ioloop
from peewee_async import Manager

from ForumApp.main_app.urls import url_patterns
from ForumApp.main_app.settings import settings, database


if __name__ == "__main__":
    # 集成json到wtfomrs中
    import wtforms_json
    wtforms_json.init()

    # 建立app
    app = web.Application(url_patterns, debug=True, **settings)
    app.listen(8888)

    # 配置async_peewee
    objects = Manager(database)
    database.set_allow_sync(False)
    app.objects = objects

    # 开始事件循环
    ioloop.IOLoop.current().start()
