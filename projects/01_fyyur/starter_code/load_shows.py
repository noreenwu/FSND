from app import *


show1 = Show(id=1,
             venue_id=1,
             artist_id=4,
             start_time="2019-05-21T21:30:00.000Z"
)

show2 = Show(id=2,
             venue_id=3,
             artist_id=5,
             start_time="2019-06-15T23:00:00.000Z"
)

show3 = Show(id=3,
             venue_id=3,
             artist_id=6,
             start_time="2035-04-01T20:00:00.000Z"
)

show4 = Show(id=4,
             venue_id=3,
             artist_id=6,
             start_time="2035-04-08T20:00:00.000Z"
)

show5 = Show(id=5,
             venue_id=3,
             artist_id=6,
             start_time="2035-04-15T20:00:00.000Z"
)


db.session.add(show1)
db.session.add(show2)
db.session.add(show3)
db.session.add(show4)
db.session.add(show5)

db.session.commit()
