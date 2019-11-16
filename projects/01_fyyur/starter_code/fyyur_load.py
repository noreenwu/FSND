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


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
#app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://noreen@localhost:5432/fyyur'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Location(db.Model):
    __tablename__ = 'Location'
    location_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    venues = db.relationship('Venue', backref=db.backref('location'), lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))   # new
    seeking_venue = db.Column(db.String(120)) # new
    seeking_description = db.Column(db.String(120))  # new
    shows = db.relationship('Show', backref=db.backref('artist'), lazy=True)


class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True)    
    start_time = db.Column('start_time', db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    # backref artist 
    # backref venue 

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))   # new
    seeking_talent = db.Column(db.String(120))  # new
    seeking_description = db.Column(db.String(120)) # new 
    location_id = db.Column(db.Integer, db.ForeignKey('Location.location_id'))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True))


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





# # delete Genres

# genres = Genre.query.all()

# for g in genres:
#     db.session.delete(g)

# db.session.commit()





artist1 = Artist(name="Guns N Petals",
    city="San Francisco",
    state="CA",
    phone="326-123-5000",
    website="https://www.gunsnpetalsband.com",
    facebook_link="https://www.facebook.com/GunsNPetals",
    seeking_venue=True,
    seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",    
)

artist2 = Artist(name="Matt Quevedo",
                 id=5,
                 city="New York",
                 state="NY",
                 phone="300-400-5000",
                 # no website
                 facebook_link="https://www.facebook.com/mattquevedo923251523",
                 seeking_venue=False,
                 image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
)                 


artist3 = Artist(name="The Wild Sax Band",
                 city="San Francisco",
                 state="CA",
                 phone="432-325-5432",
                 seeking_venue=False,
                 image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
)


db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)

db.session.commit()


venue1 = Venue(name="The Musical Hop",
               address="1015 Folsom Street",
               city="San Francisco",
               state="CA",
               phone="123-123-1234",
               website="https://www.themusicalhop.com",
               facebook_link="https://www.facebook.com/TheMusicalHop",
               seeking_talent=True,
               seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
               image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
)
venue2 = Venue(name="Park Square Live Music & Coffee",
               address="34 Whiskey Moore Ave",
               city="San Francisco",
               state="CA",
               phone="415-000-1234",
               website="https://www.parksquarelivemusicandcoffee.com",
               facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
               seeking_talent=False,
               image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
)


venueNY = Venue(name="The Dueling Pianos Bar",
                address="335 Delancey Street",
                city="New York",
                state="NY",
                phone="914-003-1132",
                website="https://www.theduelingpianos.com",
                facebook_link="https://www.facebook.com/theduelingpianos",
                seeking_talent=False,
                image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
)

db.session.add(venue1)
db.session.add(venue2)
db.session.add(venueNY)

db.session.commit()


locations = Location.query.all()

for l in locations:
    db.session.delete(l)

db.session.commit()    

location1 = Location(city="New York", state="NY")
location2 = Location(city="San Francisco", state="CA")

db.session.add(location1)
db.session.add(location2)

db.session.commit()



# # add venues to Location

locationSF = Location.query.filter_by(city="San Francisco").first()

if locationSF is not None:
    locationSF.venues.append(venue1)
    locationSF.venues.append(venue2)


db.session.commit()

locationNY = Location.query.filter_by(city="New York").first()

if locationNY is not None:
    locationNY.venues.append(venueNY)

db.session.commit()


# genre1 = Genre(name="Rock n Roll")
# genre2 = Genre(name="Jazz")
# genre3 = Genre(name="Classical")
# genre4 = Genre(name="Reggae")
# genre5 = Genre(name="Swing")
# genre6 = Genre(name="Folk")

# db.session.add(genre1)
# db.session.add(genre2)
# db.session.add(genre3)
# db.session.add(genre4)
# db.session.add(genre5)
# db.session.add(genre6)
# db.session.commit()


##  Artist <-> Venue  (many-to-many: 1 artist can have many venues; 1 venue can have many artists)
##  Artist -> Show   (one-to-many:  1 artist can have many shows; 1 show can have 1 artist)
##  Artist <-> Genre (many-to-many: 1 artist can have many genres: 1 genres can have many artists)

##  Venue -> Show (one-to-many: 1 venue can have many shows; 1 show can have 1 venue)
##  Venue <-> Genre (many-to-many: 1 venue can have many genres; 1 genre can have many venues)

##  Location -> Venue (one-to-many: 1 location can have many venues; 1 venue can have 1 location)



# # delete Shows

shows = Show.query.all()

for s in shows:
    db.session.delete(s)

db.session.commit()


show1 = Show(start_time="2019-05-21T21:30:00.000Z")

db.session.add(show1)

db.session.commit()

# query for Guns N Petals

artistGun = Artist.query.filter_by(name="Guns N Petals").first()
# rocknroll = Genre.query.filter_by(name="Rock n Roll").first()

if artistGun is not None:
    artistGun.shows.append(show1)
    # artistGun.genres.append(rocknroll)

db.session.commit()


show_sax1 = Show(start_time="2035-04-01T20:00:00.000Z")
show_sax2 = Show(start_time="2035-04-08T20:00:00.000Z")
show_sax3 = Show(start_time="2035-04-15T20:00:00.000Z")

db.session.add(show_sax1)
db.session.add(show_sax2)
db.session.add(show_sax3)

db.session.commit()

artistSax = Artist.query.filter_by(name="The Wild Sax Band").first()

if artistSax is not None:
    artistSax.shows.append(show_sax1)
    artistSax.shows.append(show_sax2)
    artistSax.shows.append(show_sax3)

db.session.commit()


#  associate shows to venues

musical_hop = Venue.query.filter_by(name="The Musical Hop").first()

if musical_hop is not None:
    musical_hop.shows.append(show1)

music_and_coffee = Venue.query.filter_by(name="Park Square Live Music & Coffee").first()
show_mc = Show(start_time="2019-06-15T23:00:00.000Z")
show_mc2 = Show(start_time="2035-04-01T20:00:00.000Z")
show_mc3 = Show(start_time="2035-04-01T20:00:00.000Z")

# db.session.add(show_mc)
# db.session.add(show_mc2)

if music_and_coffee is not None:
    music_and_coffee.shows.append(show_mc)
    music_and_coffee.shows.append(show_mc2)
    music_and_coffee.shows.append(show_mc3)



# second show (artist -> Show)

artist_quevedo = Artist.query.filter_by(name="Matt Quevedo").first()

if artist_quevedo is not None:
    artist_quevedo.shows.append(show_mc)



db.session.commit()    

shows = Show.query.all()

for s in shows:
    s.start_time
    if s.venue is not None:
        "venue ", s.venue.name
    if s.artist is not None:
        "artist ", s.artist.name



# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


