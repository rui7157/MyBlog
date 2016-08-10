#coding:utf-8
from flask import Flask
from flask_script import Shell
from flask_migrate import MigrateCommand,Migrate,Manager
from app import create_app
from app.models import db


# app=create_app()
app=create_app(__name__)
@app.route("/")
def index():
    return "test"
app.debug=True
migrate=Migrate(app,db)
manager=Manager(app)
manager.add_command("db",MigrateCommand)
if __name__ =="__main__":
    app.run()
    
