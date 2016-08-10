# -*- coding: utf-8
from . import adm
from datetime import datetime
from flask import render_template, request, session, flash, redirect, url_for, current_app,abort
from flask_login import login_user,logout_user,current_user
from functools import wraps
from ..models import Post, db, Type,User
from ..form import PostForm,LoginForm
import re
# import logging
# logging.getLogger(__name__)

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return decorated_view

@adm.route("/")
@adm.route("/index.html")
@login_required
def index():
    posts = Post.query.order_by(Post.addtime.desc())
    return render_template("admin/index.html", **locals())


@adm.route("/main.html")
@login_required
def main():
    return render_template("admin/main.html")

@login_required
@adm.route("/edit-post.html", methods=["POST", "GET"])
def new_post():
    form = PostForm()
    tags = [tag.name for tag in Type.query.order_by(Type.addtime.desc())]
    if request.method == "GET":
        pid = request.args.get("pid")
        if str(pid).isdigit():
            """编辑Post"""
            post = Post.query.get_or_404(int(pid))
            session['title'] = post.title
            session['content'] = post.content
            session['tag'] = " ".join([tag.name for tag in post.types])
            session["pid"] = pid
        elif request.args.get("type") == "new":
            """清空表单数据"""
            csrf_token = session.get("csrf_token")  # 保留csrf_token
            session.clear()
            session["csrf_token"] = csrf_token
    if request.method == "POST":
        """新建Post"""
        session['title'] = form.title.data.strip()
        session['tag'] = form.tag.data.strip() or u"杂项"
        session['content'] = form.content.data
        session['pid']=form.pid.data
        if form.validate_on_submit():
            tags = re.split(r",|，|\s+", session.get('tag').strip())
            if str(session.get('pid')).isdigit():
                post = Post.query.get_or_404(int(session.get('pid')))
                post.title = session.get('title')
                post.cont = session.get('content')
            else:
                post = Post(title=session.get('title'), cont=session.get('content'))
            db.session.add(post)
            db.session.commit()
            post.str_tags = tags
            db.session.commit()
            session.clear()
            flash(u"{}发布成功！".format(post.title))
            # return redirect(url_for("admin.new_post"))
        return redirect(url_for('admin.new_post'))
    form.title.data, form.tag.data, form.content.data,form.pid.data = session.get("title"), session.get("tag"), session.get("content"),session.get("pid")
    return render_template("admin/edit.html", form=form, tags=tags)

@login_required
@adm.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        try:
            pid = request.form.get("pid")
            db.session.delete(Post.query.get(int(pid)))
            db.session.commit()
        except Exception as e:
            current_app.logger.error('An delete post error,{} '.format(e))
            # logging.error('An delete post error:{}'.format(e))
            return "fail"
        else:
            return "success"


@adm.route("/test")
def test():
    print(current_user)
    test=current_user
    return render_template("test.html",**locals())

@adm.route("/lr",methods=["POST","GET"])
def login():
    form=LoginForm()
    if not session.get("retryTimes"):
        session['retryTimes']={"times":1}
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        isRemember=request.form.get("isRemember")
        if int(session.get("retryTimes").get("times"))%5!=0: #重试次数4次
            user=User.query.filter_by(uname=username).first()
            if user:
                if user.verif_password(password):
                #登陆成功
                    # logging.info("user:{} login".format(user.uname))
                    if isRemember:
                        login_user(user,True)
                    else:
                        login_user(user,False)
                    return redirect(url_for('admin.index'))
            flash(u"密码或用户名错误！")
            session['retryTimes']['times']+=1
            if int(session.get("retryTimes").get("times"))%5!=0:
                session["retryTimes"]["unable"]=datetime.now()
            return redirect(url_for('admin.login'))
        else:
            # logging.warning('Anonymous users repeatedly try landing failed!')
            flash(u"尝试登录次数过多请稍后再试！{}".format((datetime.now()-session.get('retryTimes').get("unable")).seconds))
            if int((datetime.now()-session.get('retryTimes').get("unable")).seconds)/60>5:
                session['retryTimes']['times']+=1
            return redirect(url_for('admin.login'))
    return render_template("admin/login.html",form=form)

@adm.route("/logout")
def logout():
    # logging.info("user:{} logout.".format(current_user.uname))
    logout_user()
    return redirect(url_for("main.index"))