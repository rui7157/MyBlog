# from . import create_app
# app=create_app()
from . import app
@app.route("/test")
def Test():
    return "test success!"