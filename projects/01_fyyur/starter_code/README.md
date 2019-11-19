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

Once the dependencies are available, run the following:

    $ export FLASK_APP=myapp
    $ export FLASK_ENV=development # enables debug mode
    $ python3 app.py


## Implementation Notes




## Required Files

app.py - the main driver of the app, starts the app up in a web server on localhost

config.py - contains the parameters for connecting to the database

models.py - contains the schema definition for both app.py and fyyur_load.py

fyyur_load.py - loads initial data into the database (also deletes old data, resulting in a fresh start)

requirements.txt - contains the dependencies needed for the app to run

forms.py - contains forms data that populates into the forms

templates - directory contains html for forms, pages and layouts required for the site

