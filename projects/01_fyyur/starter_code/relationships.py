#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import Boolean
# from models import Genre

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
#app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://noreen@localhost:5432/testmany'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


artist_venue = db.Table('artist_venue',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.artist_id')),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.venue_id'))
)


# artist_genre = db.Table('artist_genre',
#     db.Column('genre_id', db.Integer, db.ForeignKey('Genre.genre_id')),
#     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.artist_id'))
# )


class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True)    
    start_time = db.Column('start_time', db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.artist_id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.venue_id'))


class Artist(db.Model):
    __tablename__ = 'Artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    shows = db.relationship('Show', backref=db.backref('artist'), lazy=True)
    # venues = db.relationship('Venue', secondary=artist_venue, backref=db.backref('artists'))
    # genres = db.relationship('Genre', secondary=artist_genre, backref=db.backref('artists'))


class Venue(db.Model):
    __tablename__ = 'Venue'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    location_id = db.Column(db.Integer, db.ForeignKey('Location.location_id'))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True))
#    shows = db.relationship('Show', secondary=venue_show, backref=db.backref('venue'))


class Genre(db.Model):
    __tablename__ = 'Genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Location(db.Model):
    __tablename__ = 'Location'
    location_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    venues = db.relationship('Venue', backref=db.backref('location'), lazy=True)
 #   venues = db.relationship('Venue', secondary=location_venue, backref=db.backref('location'))

    