from wtforms_tornado import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired


class LoginForm(Form):
    mobile = StringField("mobile", validators=[DataRequired("请输入手机号")])
    password = StringField("password", validators=[DataRequired("请输入密码")])
