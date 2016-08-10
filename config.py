# coding:utf-8
import os


class Configuration(object):
    SECRET_KEY = "c61f1f9e762e14h654dd"
    CHARSET = 'utf8'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://2d5cdc9f4f044fa29d9ef8e37d40a09b:982f80a0d86c4acf94a444ef9fb0a2de@sqld.duapp.com:4050/DzBhYPfwAgVQexRZklPL"#"mysql+pymysql://oz5z1y2nxz:l252hiklh3jj5ymwm35z0345454lk42wmkihhzh5@r.rdc.sae.sina.com.cn:3307/app_nvray"  #os.getenv("sql",default="mysql+pymysql://root:@127.0.0.1/myblog")  
    SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    LOGGING_CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf')
    LOGGING_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'NvRayServer.log')
    POSTS_PRO_PAGINATE = 5  # 分页数量
