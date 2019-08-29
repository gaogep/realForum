import functools
import jwt

from ForumApp.apps.users.models import User


def authenticated_async(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        tsid = self.request.headers.get("tsessionid", None)
        if tsid:
            try:
                data = jwt.decode(
                    tsid, self.settings["secret_key"],
                    leeway=self.settings["jwt_expire"],
                    options={"verify_exp": True}
                )
                user_id = data["id"]
                try:
                    user = await self.applicaion.objects.get(User, id=user_id)
                    self._current_user = user
                    await method(self, *args, **kwargs)
                except User.DoesNotExist as e:
                    self.set_status(401)
            except jwt.exceptions.ExpiredSignatureError as e:
                self.set_status(401)
        else:
            self.set_status(401)
        await self.finish({})
    return wrapper
