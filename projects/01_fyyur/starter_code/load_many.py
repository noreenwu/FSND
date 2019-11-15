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

artist1 = Artist(name="Guns N Petals")           # add artist records
db.session.add(artist1)

artist2 = Artist(name="Matt Q")
db.session.add(artist2)


venue1 = Venue(name="The Dueling Pianos Bar")              # add venue records
db.session.add(venue1)

venue2 = Venue(name="Park Square Live Coffee Bar")
db.session.add(venue2)


db.session.query(Show).delete()             # delete all Show records

show1 = Show(start_time="2004-12-28 12:00:00")                 # add show records
db.session.add(show1)

show2 = Show(start_time="2008-12-12 04:00:00")
db.session.add (show2)

show3 = Show(start_time="2012-01-01 05:00:22")
db.session.add(show3)


db.session.commit()