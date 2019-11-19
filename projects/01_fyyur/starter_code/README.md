# Project: Fyyur
# Noreen Wu 
# Udacity React: November 2019

# Overview

Fyyur is a venue and artist matching site that helps performance artists find venues and venues
find performers. The tech stack includes Postgres, Flask, SQLAlchemy, Python, Jinja, HTML and CSS.

## Installation Requirements

The following must be installed in order for the app to run:

    Postgres

    Flask (sudo pip3 install Flask)

    dependencies listed in requirements.txt (pip3 install -r requirements.txt)

    Python3

Once the dependencies are available, cd into the working directory and run the following:

    $ createdb fyyur         # creates Postgres db for this app
    $ flask db init          # creates directory structure for migrations
    $ flask db migrate       # looks for changes in the schema -- the whole schema, on the first run
    $ flask db upgrade       # applies schema changes to the database
    $ python3 fyyur_load.py  # loads some initial data into the database 
    $ python3 app.py         # runs the Fyyur app on localhost:5000 (view with browser)


If fyyur_load is not loaded, then the app will run with no initial data.


## Implementation Notes

Relationships: 

In addition to enforcing data integrity through the use of constraints defined in the schema
(such as nullable=False and unique=True, and use of primary and foreign keys), identifying the one-to-many and
many-to-many relationships was key driver in structuring the data. 

In the case of one-to-one and one-to-many relationships, foreign keys were utilized (one Location has many Venues)
and in the case of many-to-many, a secondary table was defined, establishing 2 one-to-many relationships
joined by the table (artist_genre and venue_genre: an artist may have many genres, a genre may have many
artists; a venue may have many genres and a genre may have many venues). Artists may play at multiple venues
and a venue may host many performing artists; artists and venues are a many-to-many relationship that are
connected through a kind of secondary entity, the Show. Show is not a table (like artist_genre and venue_genre),
as it has a field itself: start_time. But it serves a similar function to the artist_genre and venue_genre
tables, in structuring a many-to-many relationship into 2 one-to-many relationships: one venue may
have many shows but one show has only one venue; one artist may have many shows but one show has only one artist.

Changes to templates: 

Links to Edit the venue and to Edit the artist were added to the bottom of the Artist detail and 
Venue detail pages, for convenience. Venues may be deleted by following the Delete link, also located at
the bottom of the Edit venue screen.


Error handling:

Where possible, SQLAlchemy exceptions are caught, such that failures to insert a record, whether due
to user error or database inavailability, result in a graceful exit. Examples include:
    1) not providing a valid artist ID or venue ID when adding a show
    2) adding an artist or a venue using a name that already exists
    3) failure to delete a venue
    

## Required Files

app.py - the main driver of the app, starts the app up in a web server on localhost

config.py - contains the parameters for connecting to the database

models.py - contains the schema definition for both app.py and fyyur_load.py

fyyur_load.py - loads initial data into the database (also deletes old data, resulting in a fresh start)

requirements.txt - contains the dependencies needed for the app to run

forms.py - contains forms data that populates into the forms

templates - directory contains html for forms, pages and layouts required for the site

