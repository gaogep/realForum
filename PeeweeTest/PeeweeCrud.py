from PeeweeTest.models.model import Vendors, Goods
from PeeweeTest.models.data import supplier_list, goods_list


def save_vendors():
    for s in supplier_list:
        vendor = Vendors(
            name=s["name"], address=s["address"], mobile=s["phone"]
        )
        vendor.save()


def save_goods():
    for g in goods_list:
        good = Goods(
            name=g["name"], vendor=g["supplier"], click_nums=g["click_num"],
            inventory=g["goods_num"], price=g["price"], brife_intro=g["brief"]
        )
        good.save()


save_vendors()
save_goods()
