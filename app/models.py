# coding: utf-8
from . import db, loginManager
from datetime import datetime
import bleach
import re
from werkzeug.security import generate_password_hash, check_password_hash

# from .db import db.Column, DateTime, Integer, String, Text, text,Model
try:
    from html.parser import HTMLParser
except ImportError as e:
    from HTMLParser import HTMLParser
from re import sub

db.create_all()
class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')
    def text(self):
        return ''.join(self.__text).strip()


parser = _DeHTMLParser()


class Posttype(db.Model):
    __tablename__ = 'posttype'
    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.Integer, db.ForeignKey("post.id", ondelete=True))
    typeid = db.Column(db.Integer, db.ForeignKey("type.id"))


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Integer)
    showpic = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    showcontent = db.Column(db.Text, nullable=False)  # 清除html各种标记对
    addtime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    hits = db.Column(db.Integer, nullable=False, default=0)
    types = db.relationship("Type", secondary="posttype", backref=db.backref("post_types"), passive_deletes=True)

    def __repr__(self):
        return "<post: {}>".format(self.id)

    def _find_or_create_tag(self, tag):
        t = Type.query.filter_by(name=tag).first()
        if not (t):
            t = Type(name=tag)
        return t

    @property
    def str_tags(self):
        return [tag for tag in self.types]

    @str_tags.setter
    def str_tags(self, values):
        self.types.clear()
        for tag in values:
            self.types.append(self._find_or_create_tag(tag))

    @property
    def cont(self):
        return self.content

    def tableformat(self,tableHtml):
        return re.sub("","",tableHtml)


    @cont.setter
    def cont(self, value):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'u', 'strike', 'font', 'br', 'span', 'table', 'td', 'tr', 'code', 'pre',
                        'img', 'thead', 'tbody', 'tfoot', 'iframe']
        value = bleach.linkify(bleach.clean(value, tags=allowed_tags, strip=True))
        self.content = value
        parser.feed(value)
        parser.close()
        self.showcontent = parser.text()


class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), server_default=db.text("''"), unique=True)
    addtime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posts = db.relationship("Post", secondary="posttype", backref=db.backref("type_posts"))

    def __repr__(self):
        return "<type: {}>".format(self.name)


class User(db.Model):
    """
    role：0 游客 1 管理员
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, index=True, primary_key=True)
    uname = db.Column(db.String(64), unique=True)
    hash_password = db.Column(db.String(64))
    role = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    about = db.Column(db.Text, nullable=True)

    @property
    def password(self):
        raise AttributeError("password can't read!")

    @password.setter
    def password(self, value):
        self.hash_password = generate_password_hash(value)

    def verif_password(self, pwd):
        return check_password_hash(self.hash_password, pwd)

    # is_authenticated() 如果用户已经登录，必须返回 True ，否则返回 False
    # is_active() 如果允许用户登录，必须返回 True ，否则返回 False 。如果要禁用账户，可以返回 False
    # is_anonymous() 对普通用户必须返回 False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        if self.role == 0:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<user: {}>".format(self.uname)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
