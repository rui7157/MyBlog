# -*- coding: utf-8
from ..models import Post, Type
from flask import render_template, Blueprint, request
from .. import db
from flask_sqlalchemy import sqlalchemy

adm = Blueprint("admin",__name__,template_folder="../templates/admin")
from . import home