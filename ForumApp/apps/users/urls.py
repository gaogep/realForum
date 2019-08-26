from tornado.web import url

from .handler import SendVrifyCodeHandler, LoginHandler

urlpatterns = [
    url("/code/?", SendVrifyCodeHandler, name="send_verify_code"),
    url("/login/?", LoginHandler, name="send_verify_code")
]
