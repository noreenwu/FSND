from app import *


artist1 = Artist(artist_id=4,
                 name="Guns N Petals",
 #   "genres": ["Rock n Roll"],
                 city="San Francisco",
                 state="CA",
                 phone="326-123-5000",
                 website="https://www.gunsnpetalsband.com",
                 facebook_link="https://www.facebook.com/GunsNPetals",
                 seeking_venue=True,
                 seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
                 image_link=https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
                 past_shows_count=1,
                 upcoming_shows_count=0,


)
# genre2 = Genre(genre_id=2, genre_name='Reggae')
# genre3 = Genre(genre_id=3, genre_name='Swing')
# genre4 = Genre(genre_id=4, genre_name='Classical')
# genre5 = Genre(genre_id=5, genre_name='Folk')

db.session.add(artist1)
db.session.commit()


