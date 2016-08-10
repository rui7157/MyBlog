# coding:utf-8
import os
# import sae.const


class Configuration(object):
    SECRET_KEY = "c61f1f9e762e14h654dd"
    CHARSET = 'utf8'
    SQLALCHEMY_DATABASE_URI = os.getenv("sql",default="mysql+pymysql://root:@127.0.0.1/myblog") or os.environ.get("DATABASE_URL") or "mysql+pymysql://{u}:{p}@{h}:{P}/{db}".format(u=sae.const.MYSQL_USER,p=sae.const.MYSQL_PASS,h=sae.const.MYSQL_HOST,P=sae.const.MYSQL_PORT,db=sae.const.MYSQL_DB)  #os.getenv("sql",default="mysql+pymysql://root:@127.0.0.1/myblog")  
    SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    LOGGING_CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf')
    LOGGING_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'NvRayServer.log')
    POSTS_PRO_PAGINATE = 5  # 分页数量
