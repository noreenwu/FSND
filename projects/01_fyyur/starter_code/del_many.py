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


from relationships import *


# db.session.query(Artist).delete()          # delete all Artist records

# db.session.query(Venue).delete()           # delete all Venue records

# db.session.query(Genre).delete()           # delete all Genre records

# db.session.query(Show).delete()            # delete all Show records

# db.session.query(Location).delete()        # delete all Location records

# db.session.commit()

# delete Venues

venues = Venue.query.all()

for v in venues:
    db.session.delete(v)

db.session.commit()


# delete Artists

artists = Artist.query.all()

for a in artists:
    db.session.delete(a)

db.session.commit()


# delete Shows

shows = Show.query.all()

for s in shows:
    db.session.delete(s)

db.session.commit()


# delete Genres

genres = Genre.query.all()

for g in genres:
    db.session.delete(g)

db.session.commit()


locations = Location.query.all()

for l in locations:
    db.session.delete(l)

db.session.commit()    