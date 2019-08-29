from wtforms_tornado import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, Length


class CommunityForm(Form):
    name = StringField("小组名称", validators=[DataRequired("请输入小组名称")])
    category = StringField("小组类别", validators=[AnyOf(values=["类别1", "类别2"])])
    desc = TextAreaField("小组简介", validators=[DataRequired("请输入小组简介")])
    notice = TextAreaField("小组公告", validators=[DataRequired("请输入小组公告")])


class GroupApplyForm(Form):
    apply_reason = StringField("申请理由", validators=[DataRequired("说明申请理由")])


class PostForm(Form):
    title = StringField("标题", validators=[DataRequired("请输入标题")])
    content = StringField("内容", validators=[DataRequired("请输入内容")])


class PostCommentForm(Form):
    content = StringField("评论", validators=[DataRequired("请输入评论内容"), Length(3, 200)])
