from datetime import datetime

from .settings import database
from peewee import Model, DateTimeField


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        database = database
