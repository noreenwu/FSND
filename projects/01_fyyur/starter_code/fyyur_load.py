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
from datetime import datetime

# from app import Venue, Show, Artist, venue_genre, artist_genre
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
#app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://noreen@localhost:5432/fyyur'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import *

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


### shows to artists

show_hop = Show(start_time="2019-05-21T21:30:00.000Z")

db.session.add(show_hop)

db.session.commit()

# query for Guns N Petals

artistGun = Artist.query.filter_by(name="Guns N Petals").first()
# rocknroll = Genre.query.filter_by(name="Rock n Roll").first()

if artistGun is not None:
    artistGun.shows.append(show_hop)
    # artistGun.genres.append(rocknroll)

db.session.commit()



show_sax2019 = Show(start_time="2019-06-15T23:00:00.000Z")
show_sax1 = Show(start_time="2035-04-01T20:00:00.000Z")
show_sax2 = Show(start_time="2035-04-08T20:00:00.000Z")
show_sax3 = Show(start_time="2035-04-15T20:00:00.000Z")

db.session.add(show_sax2019)
db.session.add(show_sax1)
db.session.add(show_sax2)
db.session.add(show_sax3)

db.session.commit()



# second show (artist -> Show)

artist_quevedo = Artist.query.filter_by(name="Matt Quevedo").first()

if artist_quevedo is not None:
    artist_quevedo.shows.append(show_sax2019)

artistSax = Artist.query.filter_by(name="The Wild Sax Band").first()

if artistSax is not None:
    artistSax.shows.append(show_sax1)
    artistSax.shows.append(show_sax2)
    artistSax.shows.append(show_sax3)

db.session.commit()


#  associate shows to venues

musical_hop = Venue.query.filter_by(name="The Musical Hop").first()

if musical_hop is not None:
    musical_hop.shows.append(show_hop)

ven_music_and_coffee = Venue.query.filter_by(name="Park Square Live Music & Coffee").first()
# show_mc = Show(start_time="2019-06-15T23:00:00.000Z")
# show_mc2 = Show(start_time="2035-04-01T20:00:00.000Z")  
# show_mc3 = Show(start_time="2035-04-08T20:00:00.000Z")
# show_mc4 = Show(start_time="2035-04-15T20:00:00.000Z")

# db.session.add(show_mc)
# db.session.add(show_mc2)

if ven_music_and_coffee is not None:
    ven_music_and_coffee.shows.append(show_sax2019)
    ven_music_and_coffee.shows.append(show_sax1)
    ven_music_and_coffee.shows.append(show_sax2)
    ven_music_and_coffee.shows.append(show_sax3)



db.session.commit()    



# delete Genres

genres = Genre.query.all()

for g in genres:
    db.session.delete(g)

db.session.commit()



genre_rock = Genre(name="Rock n Roll")
genre_jazz = Genre(name="Jazz")
genre_classical = Genre(name="Classical")
genre_reggae = Genre(name="Reggae")
genre_swing = Genre(name="Swing")
genre_folk = Genre(name="Folk")
genre_RB = Genre(name="R&B")
genre_hiphop = Genre(name="Hip-Hop")

db.session.add(genre_rock)
db.session.add(genre_jazz)
db.session.add(genre_classical)
db.session.add(genre_reggae)
db.session.add(genre_swing)
db.session.add(genre_folk)
db.session.add(genre_RB)
db.session.add(genre_hiphop)
db.session.commit()


venueHop = Venue.query.filter_by(name="The Musical Hop").first()

if venueHop is not None:
    venueHop.genres = [genre_jazz, genre_reggae, genre_swing, genre_classical, genre_folk]


venue_dueling = Venue.query.filter_by(name="The Dueling Pianos Bar").first()

if venue_dueling is not None:
    venue_dueling.genres = [ genre_classical, genre_RB, genre_hiphop ]


venue_music_coffee = Venue.query.filter_by(name="Park Square Live Music & Coffee").first()

if venue_music_coffee is not None:
    venue_music_coffee.genres = [ genre_rock, genre_jazz, genre_classical, genre_folk ]



db.session.commit()



# add genres to Artists

artist_petals = Artist.query.filter_by(name="Guns N Petals").first()

if artist_petals is not None:
    artist_petals.genres.append(genre_rock)


artist_matt = Artist.query.filter_by(name="Matt Quevedo").first()

if artist_matt is not None:
    artist_matt.genres.append(genre_jazz)


artist_sax = Artist.query.filter_by(name="The Wild Sax Band").first()
    
if artist_sax is not None:
    artist_sax.genres.append(genre_jazz)
    artist_sax.genres.append(genre_classical)


db.session.commit()


# shows = Show.query.all()


# class Show_Info(object):
#     start_time = ""
#     venue_id = 0
#     venue_name = ""
#     artist_id = 0
#     artist_name = ""
#     artist_image = ""

#     def __init__(self, start_time, venue_id, venue_name, artist_id, artist_name, artist_image):
#         self.start_time = start_time
#         self.venue_id = venue_id
#         self.venue_name = venue_name
#         self.artist_id = artist_id
#         self.artist_name = artist_name
#         self.artist_image = artist_image

# d = []
# for s in shows:
#     ss = {}
#     if s.venue is not None:
#         if s.artist is not None:
#             x = s.start_time
#             ss['start_time'] = x.strftime("%Y-%m-%dT%H:%M:%S.000Z")
#             ss['venue_id'] = s.venue_id
#             ss['artist_id'] = s.artist_id
#             ss['artist_name'] = s.artist.name
#             ss['artist_image_link'] = s.artist.image_link
#             d.append(ss)


#             # s_info = Show_Info(s.start_time, s.venue_id, s.venue.name, s.artist_id, s.artist.name, s.artist.image_link)
#             # s_info
#             # d.append(s_info)
#     # if s.venue is not None:
#     #     'venue_id', s.venue_id
#     #     "venue_name", s.venue.name
#     # if s.artist is not None:
#     #     "artist_id", s.artist_id
#     #     "artist_name", s.artist.name
#     #     "artist_image", s.artist.image_link

    

# print (d)


# time comparison

# for s in shows:
#     if s.start_time > datetime.now():
#        s.start_time


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


