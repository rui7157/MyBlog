#coding:utf-8
from flask import Flask
from flask_script import Shell
from flask_migrate import MigrateCommand,Migrate,Manager
from app import create_app
from app.models import db


app=create_app()
app.debug=True


migrate=Migrate(app,db)
manager=Manager(app)
manager.add_command("db",MigrateCommand)
def make_shell_context():
    return dict(app=app,db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ =="__main__":
    app.run('0.0.0.0',port=5000)
    
