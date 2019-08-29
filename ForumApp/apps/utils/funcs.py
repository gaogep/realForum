from datetime import date, datetime


# 解决时间类型无法序列化的问题
def json_serialize(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} is not serializable")
