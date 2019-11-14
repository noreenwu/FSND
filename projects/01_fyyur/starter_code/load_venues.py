from app import *



v1 = Venue(id=1,
            name="The Musical Hop",
            address="1015 Folsom Street",
            city="San Francisco",
            state="CA",
            phone="123-123-1234",
            website="https://www.themusicalhop.com",
            facebook_link="https://www.facebook.com/TheMusicalHop",
            seeking_talent=True,
            seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
            image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            past_shows_count=1,
            upcoming_shows_count=0
            )

v2 = Venue(id=2,
            name="The Dueling Pianos Bar",
            address="335 Delancey Street",
            city="New York",
            state="NY",
            phone="914-003-1132",
            website="https://www.theduelingpianos.com",
            facebook_link="https://www.facebook.com/theduelingpianos",
            seeking_talent=False,
            image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
            past_shows_count=0,
            upcoming_shows_count=0)

v3 = Venue(id=3,
            name="Park Square Live Music & Coffee",
            address="34 Whiskey Moore Ave",
            city="San Francisco",
            state="CA",
            phone="415-000-1234",
            website="https://www.parksquarelivemusicandcoffee.com",
            facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            seeking_talent=False,
            image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
)
db.session.add(v1)
db.session.add(v2)
db.session.add(v3)
db.session.commit()

# v1.artists.append(artist1)
# v3.artists.append(artist2)
# v3.artists.append(artist3)
# v3.artists.append(artist3)    # again with different start time
