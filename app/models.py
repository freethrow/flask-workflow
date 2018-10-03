#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app, request, url_for
from datetime import datetime
import hashlib

from flask_login import UserMixin, AnonymousUserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##############################################################
class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean(),default=False)
  
    @property
    def password(self):

        raise AttributeError('password not readable')

    @password.setter
    def password(self,password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        try:
            return check_password_hash(self.password_hash, password)
        except AttributeError:
            return False

    def __repr__(self):
        return unicode(self.username)


class Gallery(db.Model):

    __tablename__ = 'galleries'

    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime(), default=datetime.now)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    pictures = db.relationship('Picture', backref='pictures',
                                lazy='dynamic')
    
    def __repr__(self):

        return u"Gallery name: {0}".format(self.title)


class Picture(db.Model):

    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime(), default=datetime.now)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.id'))
    gallery = db.relationship('Gallery',  foreign_keys=[gallery_id])
    title = db.Column(db.String)
    description = db.Column(db.Text)
    filename = db.Column(db.String)
    thumb = db.Column(db.String)
    bw_thumb = db.Column(db.String)

    def __repr__(self):

        return u"Picture name: {0} / gallery: {1}".format(self.title, self.gallery.title)




