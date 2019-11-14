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


##  Artist <-> Venue  (many-to-many: 1 artist can have many venues; 1 venue can have many artists)
##  Artist -> Show   (one-to-many:  1 artist can have many shows; 1 show can have 1 artist)
##  Artist <-> Genre (many-to-many: 1 artist can have many genres: 1 genres can have many artists)

##  Venue -> Show (one-to-many: 1 venue can have many shows; 1 show can have 1 venue)
##  Venue <-> Genre (many-to-many: 1 venue can have many genres; 1 genre can have many venues)

##  Location -> Venue (one-to-many: 1 location can have many venues; 1 venue can have 1 location)



# add venues to SF Location

locationSF = Location.query.filter_by(city="San Francisco").first()
venueInSF = Venue(name="The Musical Hop")
venueInSF2 = Venue(name="Park Square Live Music & Coffee")

locationSF.venues.append(venueInSF)
locationSF.venues.append(venueInSF2)

db.session.commit()

# add venues to NY Location
venueInNY = Venue(name="The Dueling Pianos Bar")

locationNY = Location.query.filter_by(city="New York").first()
locationNY.venues.append(venueInNY)


  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }


#  an individual venue venue/<venueid>

venue = Venue.query.filter_by(venue_id=1)

# filter venue.shows to get past shows
# compute past_shows_count and upcoming_shows_count (depends on current date/time)



  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]


shows = Show.query.all()

for s in shows:
   data[venue_id] = s.venue.venue_id
   data[venue_name] s.venue.name
   data[artist_id] = s.artist.artist_id
   data[artist_name] = s.artist.name
   data[start_time] = s.start_time





















