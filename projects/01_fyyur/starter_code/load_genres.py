from app import *


genre1 = Genre(genre_id=1, genre_name='Jazz')
genre2 = Genre(genre_id=2, genre_name='Reggae')
genre3 = Genre(genre_id=3, genre_name='Swing')
genre4 = Genre(genre_id=4, genre_name='Classical')
genre5 = Genre(genre_id=5, genre_name='Folk')

db.session.add(genre1)
db.session.add(genre2)
db.session.add(genre3)
db.session.add(genre4)
db.session.add(genre5)

db.session.commit()


