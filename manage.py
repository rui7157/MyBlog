from flask import Flask
from flask_script import Shell
from flask_migrate import MigrateCommand,Migrate,Manager
from app import create_app
from app.models import db


# app=create_app()
app=Flask(__name__)
@app.route("/")
def index():
    return u"第一页"

@app.route("/2")
def index2():
    return u"第二页"

app.debug=True
migrate=Migrate(app,db)
manager=Manager(app)
manager.add_command("db",MigrateCommand)
if __name__ =="__main__":
    app.run()
    
