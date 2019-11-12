from app import *


artist1 = Artist(id=4,
                 name="Guns N Petals",
 #   "genres": ["Rock n Roll"],
                 city="San Francisco",
                 state="CA",
                 phone="326-123-5000",
#                 website="https://www.gunsnpetalsband.com",
                 facebook_link="https://www.facebook.com/GunsNPetals",
                 seeking_venue=True,
                 seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
                 image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
                 past_shows_count=1,
                 upcoming_shows_count=0,
)

artist2 = Artist(
    id=5,
    name="Matt Quevedo",
    # genres=["Jazz"],
    city="New York",
    state="NY",
    phone="300-400-5000",
    facebook_link="https://www.facebook.com/mattquevedo923251523",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    past_shows_count=1,
    upcoming_shows_count=0
)

artist3=Artist(
    id=6,
    name="The Wild Sax Band",
#    "genres": ["Jazz", "Classical"],
    city="San Francisco",
    state="CA",
    phone="432-325-5432",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    past_shows_count=0,
    upcoming_shows_count=3
)

db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)
db.session.commit()
