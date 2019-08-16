from datetime import datetime

from peewee import *

db = MySQLDatabase('rfm', host='127.0.0.1', port=3306, user='root', password='123')


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        database = db


class Vendors(BaseModel):
    name = CharField(max_length=30, verbose_name="供应商名称", index=True)
    address = CharField(max_length=100, verbose_name="联系地址")
    mobile = CharField(max_length=11, verbose_name="联系方式")

    class Meta:
        table_name = 'vendors'


class Goods(BaseModel):
    vendor = ForeignKeyField(Vendors, verbose_name="供应商", backref="goods")
    name = CharField(max_length=50, verbose_name="商品名称", index=True)
    click_nums = IntegerField(default=0, verbose_name="点击数")
    inventory = IntegerField(default=0, verbose_name="商品库存")
    price = FloatField(default=0, verbose_name="商品价格")
    brief_intro = TextField(default="", verbose_name="商品简介")

    class Meta:
        table_name = 'goods'


def init_tables():
    db.create_tables([Goods, Vendors])


if __name__ == "__main__":
    init_tables()
