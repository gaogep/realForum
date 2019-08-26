import json
import jwt
from datetime import datetime

from .models import User
from .forms import LoginForm
from ForumApp.main_app.handler import RedisHandler


class SendVrifyCodeHandler(RedisHandler):
    pass


class LoginHandler(RedisHandler):
    async def post(self):
        json_response = {}
        params = self.request.body.decode("utf8")
        params = json.loads(params)
        form = LoginForm.from_json(params)
        if form.validate():
            mobile = form.mobile.data
            password = form.mobile.data
            try:
                user = await self.application.objects.get(User, mobile=mobile, password=password)
                if not user:
                    self.set_status(400)
                    json_response["non_fields"] = "用户名或密码错误"
                else:
                    payload = {
                        "id": user.id,
                        "nick_name": user.nick_name if user.nick_name else user.mobile,
                        "exp": datetime.utcnow()
                    }
                    token = jwt.encode(payload, self.settings['secjson_response_key'], algorithm='HS256')
                    json_response["id"] = user.id
                    json_response["token"] = token.decode("utf8")
            except User.DoesNotExist:
                self.set_status(400)
                json_response["mobile"] = "用户不存在"
            await self.finish(json_response)

