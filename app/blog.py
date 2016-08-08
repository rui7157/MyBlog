#coding:utf-8
from .models import Post, Type
from flask import render_template, Blueprint, request, current_app
from . import db
from sqlalchemy.exc import InternalError
import logging

main = Blueprint("main", __name__)
logging.getLogger(__name__)
MONTH = {
    1: u"一月",
    2: u"二月",
    3: u"三月",
    4: u"四月",
    5: u"五月",
    6: u"六月",
    7: u"七月",
    8: u"八月",
    9: u"九月",
    10: u"十月",
    11: u"十一月",
    12: u"十二月",
}
REVMONTH = {v: k for k, v in MONTH.items()}


def get_container_data():
    """获取数据"""
    posts = Post.query.order_by(Post.addtime.desc())
    types = Type.query.all()
    post_archives = [u"{} {}".format(t.addtime.strftime("%Y"), MONTH.get(int(t.addtime.strftime("%m")))) for t in
                     posts.all()]
    archives = dict()
    for post_time in post_archives:
        if archives.get(post_time) is None:
            archives[post_time] = 1
        else:
            archives[post_time] += 1
    return posts.limit(5).all(), types, archives


@main.route('/index.html')
@main.route('/')
def index():
    posts = Post.query.order_by(Post.addtime.desc())
    recent_posts, types, archives = get_container_data()
    return render_template("index.html", posts=posts, recent_posts=recent_posts, types=types, archives=archives)


@main.route("/about/")
def about():
    return render_template("about.html")


@main.route("/full-width/", methods=["GET", "POST"])
def fullwidth():
    recent_posts, types, archives = get_container_data()
    classify = request.args.get("classify")
    category_id = request.args.get("category", type=int)
    page = request.args.get("page", 1, type=int)
    pagination=None
    if request.method == "POST":
        page = request.form.get("page", 1, type=int)
    if classify:
        # 月份字典键，值互换
        try:
            year, zh_month = classify.split(" ")
        except ValueError as e:
            logging.error("user defined url month error:{}".format(e))
        else:
            num_month = REVMONTH.get(zh_month)
            if num_month:
                try:
                    posts = db.session.query(Post).filter(
                            Post.addtime >= "{}-{}-01".format(year, num_month)).filter(
                            Post.addtime <= "{}-{}-31".format(year, num_month))
                except InternalError as e:
                    logging.error("sqlalchemy date query error:{}".format(e))
    elif str(category_id).isdigit():
        # 按tag查询
        posts = Type.query.get(int(category_id)).post_types
    else:
        pagination = Post.query.order_by(Post.addtime.desc()).paginate(page, per_page=current_app.config.get(
                "POSTS_PRO_PAGINATE"), error_out=False)
        posts = pagination.items
    return render_template("full-width.html", posts=posts, recnet_posts=recent_posts, types=types, archives=archives,
                           pagination=pagination)


@main.route("/posts", methods=["POST"])
def posts():
    return "DDDDD"


@main.route("/single/<int:id>.html")
def single(id):
    recent_posts, types, archives = get_container_data()
    single_post = Post.query.get_or_404(id)
    single_post.hits += 1
    db.session.add(single_post)
    db.session.commit()
    return render_template("single.html", recent_posts=recent_posts, types=types, archives=archives,
                           single_post=single_post)


@main.route("/contact/")
def contact():
    return render_template("contact.html")
