from flask_sqlalchemy import SQLAlchemy

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


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
    name = db.Column(db.String(20), nullable=False)
    # backref artists
    # backref venues

class Location(db.Model):
    __tablename__ = 'Location'
    location_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    venues = db.relationship('Venue', backref=db.backref('location'), lazy=True)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))   # new
    seeking_talent = db.Column(db.Boolean)  # new
    seeking_description = db.Column(db.String(120)) # new 
    location_id = db.Column(db.Integer, db.ForeignKey('Location.location_id'))
    shows = db.relationship('Show', cascade="all,delete", backref=db.backref('venue', lazy=True))
    genres = db.relationship('Genre', secondary=venue_genre, backref=db.backref('venues'), lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
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


class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True)    
    start_time = db.Column('start_time', db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    # backref artist 
    # backref venue 