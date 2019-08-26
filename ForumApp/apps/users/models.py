from peewee import CharField, TextField, BooleanField
from ForumApp.main_app.models import BaseModel


class User(BaseModel):
    mobile = CharField(max_length=11, verbose_name="手机号码", index=True)
    password = CharField(max_length=30, verbose_name="密码")
    nick_name = CharField(max_length=20, verbose_name="昵称", null=True)
    address = CharField(max_length=200, verbose_name="地址", null=True)
    desc = TextField(null=True, verbose_name="个人简介")
    gender = BooleanField(default=True, verbose_name="性别")
