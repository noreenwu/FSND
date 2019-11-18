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
from datetime import datetime
from sqlalchemy import exc

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
artist_genre = db.Table('artist_genre',
     db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id')),
     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'))
)

venue_genre = db.Table('venue_genre',
     db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id')),
     db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'))
)

class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    # backref artists
    # backref venues

class Location(db.Model):
    __tablename__ = 'Location'
    location_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    venues = db.relationship('Venue', backref=db.backref('location'), lazy=True)


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
    seeking_talent = db.Column(db.Boolean)  # new
    seeking_description = db.Column(db.String(120)) # new 
    location_id = db.Column(db.Integer, db.ForeignKey('Location.location_id'))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True))
    genres = db.relationship('Genre', secondary=venue_genre, backref=db.backref('venues'), lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))   # new
    seeking_venue = db.Column(db.Boolean) # new
    seeking_description = db.Column(db.String(120))  # new
    shows = db.relationship('Show', backref=db.backref('artist'), lazy=True)
    genres = db.relationship('Genre', secondary=artist_genre, backref=db.backref('artists'), lazy=True)

    def __repr__(self):
        return f'<Artist {self.id}, {self.name}>'



    # TODO: implement any missing fields, as a database migration using Flask-Migrate



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True)    
    start_time = db.Column('start_time', db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    # backref artist 
    # backref venue 


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
#  Get Show Data for Artist Page
#----------------------------------------------------------------------------#
def get_artist_show_data(show_ary):
  data = []

  for cs in show_ary:
     cs_obj = { 'venue_id': cs.venue_id,
                'venue_name': cs.venue.name,
                'venue_image_link': cs.venue.image_link,
                'start_time': cs.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
              }
     data.append(cs_obj)

  return data


#----------------------------------------------------------------------------#
#  Get Show Data for Venue Page
#----------------------------------------------------------------------------#
def get_venue_show_data(show_ary):
  data = []

  for cs in show_ary:
     cs_obj = { 'artist_id': cs.artist_id,
                'artist_name': cs.artist.name,
                'artist_image_link': cs.artist.image_link,
                'start_time': cs.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
              }
     data.append(cs_obj)

  return data

#----------------------------------------------------------------------------#
#  Sort a Shows Array into Past and Upcoming Shows
#----------------------------------------------------------------------------#
def sort_shows(shows):
  present = datetime.now()

  upcoming_shows =[]
  past_shows = []

  for s in shows:
    if s.start_time > present:
        upcoming_shows.append(s)
    else:
        past_shows.append(s)  

  return past_shows, upcoming_shows        

#----------------------------------------------------------------------------#
#  Given Array of Shows Return Number of Upcoming Shows
#----------------------------------------------------------------------------#
def num_upcoming_shows(shows):
  present = datetime.now()

  past_shows, upcoming_shows = sort_shows(shows)

  return len(upcoming_shows)

#----------------------------------------------------------------------------#
#  Given a Search Term, Return a Lower Case Version, Enclosed with %
#----------------------------------------------------------------------------#
def get_term(term):    
  term_lower = term.lower()
  term_lower = '%' + term_lower + '%'
  return term_lower

#----------------------------------------------------------------------------#
#  Given List of Genre Names from Form, Return Corresponding Genre Objects from DB
#----------------------------------------------------------------------------#
def get_genre_from_db(genre_list):
  g_list = []

  for gen in genre_list:
    genre_obj = Genre.query.filter_by(name=gen).first()
    if genre_obj is None:
      # add to db
      new_genre_obj = Genre(name=gen)
      db.session.add(new_genre_obj)
      db.session.commit()
      g_list.append(new_genre_obj)
    else:
      g_list.append(genre_obj)

  return g_list

#----------------------------------------------------------------------------#
#  Given List of Genre Objects, Return Corresponding Genre Names
#----------------------------------------------------------------------------#
def get_genre_names(genre_list):
  genre_name_list = []
  for g in genre_list:
    genre_name_list.append(g.name)

  return genre_name_list  

#----------------------------------------------------------------------------#
# Return Location ID, depending on whether city or state has changed
#----------------------------------------------------------------------------#
def get_location_id(venue_id, old_city, old_state, new_city, new_state):
  
  if (old_city != new_city) or (old_state != new_state):
    # find or create a new location id
    new_location = Location.query.filter_by(city=new_city, state=new_state).first()

    if new_location is None:
        # create new location first, then get id
        new_location = Location(city=new_city, state=new_state)
        db.session.add(new_location)
        db.session.commit()
        new_location = Location.query.filter_by(city=new_city, state=new_state).first()

    return new_location.location_id

  else:
    same_location = Location.query.filter_by(city=old_city, state=old_state).first()
    logging.warning('same location was ', old_city, old_state)
    return same_location.location_id


#----------------------------------------------------------------------------#
# Get Venue Data for Venue Listing Display
#----------------------------------------------------------------------------#
def get_venue_data(venues):

  venues_extract_list = []

  for v in venues:
    v_obj = { 'id': v.id,
              'name': v.name,
              'num_upcoming_shows': num_upcoming_shows(v.shows)
            }
    venues_extract_list.append(v_obj)

  logging.warning("venue extract", venues_extract_list)
  return venues_extract_list

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')



#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  locations = Location.query.all()

  for l in locations:
    if len(l.venues) > 0:                     # don't display locations with no venues
      data.append({ 'city' : l.city, 
                    'state' : l.state,
                    'venues' : get_venue_data(l.venues)
                  })
  

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # case-insensitive search on database for artists with partial string search. 
  # searching for Hop yields "The Musical Hop".
  # searching for "Music" yields "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = get_term(request.form['search_term'])

  venue_matches = Venue.query.filter(Venue.name.ilike(search_term)).all() 

  data = []
  
  for v in (venue_matches):
    v_obj = {
      'id': v.id,
      'name': v.name,
      'num_upcoming_shows': num_upcoming_shows(v.shows)
    }
    data.append(v_obj)

  response={
    'count': len(venue_matches),
    'data': data
  }


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id

  the_venue = Venue.query.filter_by(id=venue_id).first()

  past_shows, upcoming_shows = sort_shows(the_venue.shows)

  data = {
     'id': the_venue.id,
     'name': the_venue.name,
     'address': the_venue.address,
     'city': the_venue.city,
     'state': the_venue.state,
     'phone': the_venue.phone,
     'website': the_venue.website,
     'facebook_link': the_venue.facebook_link,
     'seeking_talent': the_venue.seeking_talent,
     'seeking_description': the_venue.seeking_description,
     'image_link': the_venue.image_link
  }

  data['upcoming_shows'] = get_venue_show_data(upcoming_shows)
  data['past_shows'] = get_venue_show_data(past_shows)

  data['upcoming_shows_count'] = len(upcoming_shows)
  data['past_shows_count'] = len(past_shows)

  genre_names = map(lambda x: x.name, the_venue.genres)
  data['genres'] = list(genre_names)

  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  # data = list(filter(lambda d: d['id'] == venue_id, data))[0]

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  genres = get_genre_from_db(request.form.getlist('genres'))

  location = Location.query.filter_by(city=request.form['city'], state=request.form['state'] ).first()

      
  new_venue = Venue(name = request.form['name'],
                    city = request.form['city'],
                    state = request.form['state'],
                    address = request.form['address'],
                    phone = request.form['phone'],
                    #image_link = 'https://unsplash.com/photos/MTO5SmPraX4'
                    facebook_link = request.form['facebook_link'],
                    image_link = 'http://westsideparentsource.org/open/oleg-kuzmin-kTA1roYnTjY-unsplash.jpg',
                    genres = genres
  )
  db.session.add(new_venue)
  db.session.commit()

  if location is None:
    # insert new location into db
    new_location = Location(city=request.form['city'],
                            state=request.form['state'],
                            venues=[ new_venue ] 
    )

    db.session.add(new_location)
  else:
    # location exists, just update venues
    location.venues.append(new_venue)

  db.session.commit()    


  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for a in artists:
      data.append({'id': a.id, 'name': a.name})

  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = get_term(request.form['search_term'])

  artist_matches = Artist.query.filter(Artist.name.ilike(search_term)).all()

  data = []

  for a in artist_matches:
     a_obj = {
       'id': a.id,
       'name': a.name,
       'num_upcoming_shows': num_upcoming_shows(a.shows)
     }
     data.append(a_obj)
  
  response={
     'count': len(artist_matches),
     'data': data
  }
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 1,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real venue data from the artist table, using artist_id

  the_artist = Artist.query.filter_by(id=artist_id).first()

  data = {
    'id': the_artist.id,
    'name': the_artist.name,
    'city': the_artist.city,
    'state': the_artist.state,
    'phone': the_artist.phone,
    'website': the_artist.website,
    'facebook_link': the_artist.facebook_link,
    'seeking_venue': the_artist.seeking_venue,
    'seeking_description': the_artist.seeking_description,
    'image_link': the_artist.image_link,
  }

  past_shows, upcoming_shows = sort_shows(the_artist.shows)

  data['past_shows'] = get_artist_show_data(past_shows)
  data['upcoming_shows'] = get_artist_show_data(upcoming_shows)

  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  genre_names = map(lambda x: x.name, the_artist.genres)
  data['genres'] = list(genre_names)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.filter_by(id=artist_id).first()

  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = get_genre_names(artist.genres)
  form.facebook_link.data = artist.facebook_link

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  the_artist = Artist.query.filter_by(id=artist_id).first()
  genres_from_db = get_genre_from_db(request.form.getlist('genres'))

  the_artist.name = request.form['name']
  the_artist.city = request.form['city']
  the_artist.state = request.form['state']
  the_artist.phone = request.form['phone']
  the_artist.genres = get_genre_from_db(request.form.getlist('genres'))
  the_artist.facebook_link = request.form['facebook_link']

  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.filter_by(id=venue_id).first()

  genre_names = get_genre_names(venue.genres)
  logging.warning("venue form genre names ", genre_names)

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.facebook_link.data = venue.facebook_link
  form.genres.data = genre_names

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  the_venue = Venue.query.filter_by(id=venue_id).first()

  genres_from_db = get_genre_from_db(request.form.getlist('genres'))

  the_venue.location_id = get_location_id(venue_id, the_venue.city, the_venue.state, request.form['city'], request.form['state'])
  the_venue.name = request.form['name']
  the_venue.city = request.form['city']
  the_venue.state = request.form['state']
  the_venue.address = request.form['address']
  the_venue.phone = request.form['phone']
  the_venue.facebook_link = request.form['facebook_link']
  the_venue.genres = genres_from_db

  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()


  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form

  genres = get_genre_from_db(request.form.getlist('genres'))

  new_artist = Artist(name=request.form['name'],
                      city=request.form['city'],
                      state=request.form['state'],
                      phone=request.form['phone'],
                      facebook_link=request.form['facebook_link'],
                      image_link = 'http://westsideparentsource.org/open/oleg-kuzmin-kTA1roYnTjY-unsplash.jpg',
                      genres=genres
                      )

  db.session.add(new_artist)                      
  db.session.commit()

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  the_shows = Show.query.order_by(Show.start_time).all()
  data = []
  for s in the_shows:
      ss = {}
      if s.venue is not None:
          if s.artist is not None:
              x = s.start_time
              ss['start_time'] = x.strftime("%Y-%m-%dT%H:%M:%S.000Z")
              ss['venue_id'] = s.venue_id
              ss['venue_name'] = s.venue.name
              ss['artist_id'] = s.artist_id
              ss['artist_name'] = s.artist.name
              ss['artist_image_link'] = s.artist.image_link
              data.append(ss)


  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form


  artist = Artist.query.filter_by(id=request.form['artist_id']).first()
  venue = Venue.query.filter_by(id=request.form['venue_id']).first()

  # return an error if the user puts in an invalid id for artist or venue
  if artist is None:
    return render_template('errors/500-invalid-id.html'), 500

  if venue is None:
    return render_template('errors/500-invalid-id.html'), 500


  new_show = Show(start_time=request.form['start_time'],
                  venue_id=request.form['venue_id'],
                  artist_id=request.form['artist_id']
                  )

  db.session.add(new_show)

  try:
    db.session.commit()
  except exc.SQLAlchemyError:
    flash('Uh oh -- something went wrong. Show was not listed')

  # on successful db insert, flash success
  flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
