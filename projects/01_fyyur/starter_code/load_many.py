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



from appmany import *

db.session.query(Artist).delete()          # delete all Artist records

artist1 = Artist(name="artist1")           # add artist records
db.session.add(artist1)

artist2 = Artist(name="artist2")
db.session.add(artist2)


db.session.query("location_venue").delete()

db.session.query(Location).delete()        # delete all Location records

db.session.query(Venue).delete()           # delete all Venue records

venue1 = Venue(name="venue1")              # add venue records
db.session.add(venue1)

venue2 = Venue(name="venue2")
db.session.add(venue2)


db.sesion.query(Show).delete()             # delete all Show records

show1 = Show(name="show1")                 # add show records
db.session.add(show1)

show2 = Show(name="show2")
db.session.add (show2)

show3 = Show(name="show3")
db.session.add(show3)


db.session.commit()