# -*- coding: utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class PostForm(Form):
    pid=StringField()
    title = StringField(u"标题", validators=[DataRequired(u"请填写正确格式的标题！")])
    tag = StringField(u"标签")
    content = TextAreaField(u"内容", validators=[DataRequired(u"请注意输入格式！")])


class LoginForm(Form):
    username = StringField(u"用户名", validators=[DataRequired(u"请填写正确格式的标题！")])
    password = PasswordField(u"密码", validators=[DataRequired(u"请填写正确格式的标题！")])
    isRemember = BooleanField(u"记住")
