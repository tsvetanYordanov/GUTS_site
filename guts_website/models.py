# MODELS
# =============================================
# Describes the modules used in the application.
# Each class represents a table, each instant variable - a column

import hashlib

from guts_website import db
from sqlalchemy import Table, Column, Integer, ForeignKey,create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from collections import OrderedDict

from sensitive import HASH_SALT


class DictSerializable(object):
    def dump_datetime(table, value):
        if value is None:
            return None
        return [value.strftime("%Y-%m-%d %H:%M:%S")]

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if (key == "dtstart" or key == "dtend"):
                result[key] = self.dump_datetime(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result
        
memb_event = db.Table('memb_event',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class Member(db.Model, DictSerializable):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=True)
    gumail = db.Column(db.Boolean, unique=False)
    sub_meetings = db.Column(db.Boolean, unique=False, default=True)
    sub_hackathon = db.Column(db.Boolean, unique=False, default=True)
    write_key = db.Column(db.String(80), unique=False)
    
    events = db.relationship('Event',
                   secondary=memb_event,
                   backref=db.backref('members', lazy='dynamic'))

    def __init__(self, fullname, email, gumail):
        self.fullname = fullname
        self.email = email
        self.gumail = gumail
        self.write_key = hashlib.sha1(email+HASH_SALT).hexdigest()

    def __repr__(self):
        return '<Email %r>' % self.email

class Event(db.Model, DictSerializable):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=False)
    icon = db.Column(db.String(200), unique=False)
    dtstart = db.Column(db.DateTime(), unique=False)
    dtend = db.Column(db.DateTime(), unique=False)
    location = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(1500), unique=False)
    fb_event = db.Column(db.String(20), unique=False)
    map_query = db.Column(db.String(100), unique=False)
    
    def __init__(self, title, icon, dtstart, dtend, location, description, fb_event, map_query):
        self.title = title
        self.icon = icon
        self.dtstart = dtstart
        self.dtend = dtend
        self.location = location
        self.description = description
        self.fb_event = fb_event
        self.map_query = map_query


    def __repr__(self):
       return '<Event %r>' % self.id
    

pro_tech = db.Table('pro_tech',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('technology_id', db.Integer, db.ForeignKey('technology.id'))
)

pro_plat = db.Table('pro_plat',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'))
)

class Project(db.Model, DictSerializable):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    author = db.Column(db.String(120), unique=False)
    contact = db.Column(db.String(120), unique=False)
    website = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(1000), unique=False)
    icon = db.Column(db.String(100), unique=False)
    
    technologies = db.relationship('Technology',
                   secondary=pro_tech,
                   backref=db.backref('projects', lazy='dynamic'))

    def __init__(self, title, author, contact, website, description, icon):
        self.title = title
        self.author = author
        self.contact = contact
        self.website = website
        self.description = description
        self.icon = icon

    def __repr__(self):
        return '<name %r>' % self.title

class Technology(db.Model, DictSerializable):
    __tablename__ = 'technology'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    website = db.Column(db.String(120), unique=True)

    def __init__(self, name, website):
        self.name = name
        self.website = website

    def __repr__(self):
        return '<name %r>' % self.name
        
class Platform(db.Model, DictSerializable):
    __tablename__ = 'platform'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<name %r>' % self.name



















