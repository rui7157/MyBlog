from bae.core.wsgi import WSGIApplication
from manage import app
application = WSGIApplication(app)