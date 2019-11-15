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


artist_genre = db.Table('artist_genre',
     db.Column('genre_id', db.Integer, db.ForeignKey('Genre.genre_id')),
     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.artist_id'))
)


class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True)    
    start_time = db.Column('start_time', db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.artist_id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.venue_id'))
    # backref artist 
    # backref venue 

class Artist(db.Model):
    __tablename__ = 'Artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    shows = db.relationship('Show', backref=db.backref('artist'), lazy=True)
    venues = db.relationship('Venue', secondary=artist_venue, backref=db.backref('artists'))
    genres = db.relationship('Genre', secondary=artist_genre, backref=db.backref('artists'))


class Venue(db.Model):
    __tablename__ = 'Venue'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(130))
    location_id = db.Column(db.Integer, db.ForeignKey('Location.location_id'))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True))
    # backref artists
    # backref location

class Genre(db.Model):
    __tablename__ = 'Genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    # backref artists

class Location(db.Model):
    __tablename__ = 'Location'
    location_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    # venue_id = db.Column(db.Integer, db.ForeignKey('Venue.venue_id'))
    venues = db.relationship('Venue', backref=db.backref('location'), lazy=True)

db.create_all()
    

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


artist1 = Artist(name="Guns N Petals")
artist2 = Artist(name="Pamela G")
artist3 = Artist(name="The Wild Sax Band")

db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)

db.session.commit()


venue1 = Venue(name="The Musical Hop")
venue2 = Venue(name="Park Square Live Music & Coffee")
venueNY = Venue(name="The Dueling Piano Bar")

db.session.add(venue1)
db.session.add(venue2)
db.session.add(venueNY)

db.session.commit()

show1 = Show(start_time="2019-09-15 20:00:00")
show2 = Show(start_time="2018-08-08 19:00:00")
show3 = Show(start_time="2019-12-12 21:00:00")

db.session.add(show1)
db.session.add(show2)
db.session.add(show3)

db.session.commit()

location1 = Location(city="New York", state="NY")
location2 = Location(city="San Francisco", state="CA")

db.session.add(location1)
db.session.add(location2)


genre1 = Genre(name="Rock")
genre2 = Genre(name="Reggae")

db.session.add(genre1)
db.session.add(genre2)

db.session.commit()


##  Artist <-> Venue  (many-to-many: 1 artist can have many venues; 1 venue can have many artists)
##  Artist -> Show   (one-to-many:  1 artist can have many shows; 1 show can have 1 artist)
##  Artist <-> Genre (many-to-many: 1 artist can have many genres: 1 genres can have many artists)

##  Venue -> Show (one-to-many: 1 venue can have many shows; 1 show can have 1 venue)
##  Venue <-> Genre (many-to-many: 1 venue can have many genres; 1 genre can have many venues)

##  Location -> Venue (one-to-many: 1 location can have many venues; 1 venue can have 1 location)



# add venues to SF Location

locationSF = Location.query.filter_by(city="San Francisco").first()

if locationSF is not None:
    locationSF.venues.append(venue1)
    locationSF.venues.append(venue2)


db.session.commit()

locationNY = Location.query.filter_by(city="New York").first()

if locationNY is not None:
    locationNY.venues.append(venueNY)

db.session.commit()



# show
show1 = Show(start_time="2019-05-21T21:30:00.000Z")

db.session.add(show1)

db.session.commit()

# query for Guns N Petals

artistGun = Artist.query.filter_by(name="Guns N Petals").first()

if artistGun is not None:
    artistGun.shows.append(show1)

db.session.commit()


sax1 = Show(start_time="2035-04-01T20:00:00.000Z")
sax2 = Show(start_time="2035-04-08T20:00:00.000Z")
sax3 = Show(start_time="2035-04-15T20:00:00.000Z")

db.session.add(sax1)
db.session.add(sax2)
db.session.add(sax3)

db.session.commit()

artistSax = Artist.query.filter_by(name="The Wild Sax Band").first()

if artistSax is not None:
    artistSax.shows.append(sax1)
    artistSax.shows.append(sax2)
    artistSax.shows.append(sax3)

db.session.commit()


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


