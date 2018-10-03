#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import login_required, current_user

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"You have to be logged in!"

from .models import User, Gallery, Picture

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    return app
