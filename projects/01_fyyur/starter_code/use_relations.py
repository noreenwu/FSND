from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)

from relationships import *

artist1 = Artist(name="Guns and Petals")
artist2 = Artist(name="Pamela G")

db.session.add(artist1)
db.session.add(artist2)

venue1 = Venue(name="Venue 1")
venue2 = Venue(name="Venue 2")

db.session.add(venue1)
db.session.add(venue2)


show1 = Show(start_time="2019-09-15 20:00:00")
show2 = Show(start_time="2018-08-08 19:00:00")
show3 = Show(start_time="2019-12-12 21:00:00")

db.session.add(show1)
db.session.add(show2)
db.session.add(show3)

location1 = Location(city="New York", state="NY")
location2 = Location(city="San Fran", state="CA")

db.session.add(location1)
db.session.add(location2)


genre1 = Genre(name="Rock")
genre2 = Genre(name="Reggae")

db.session.add(genre1)
db.session.add(genre2)

db.session.commit()


