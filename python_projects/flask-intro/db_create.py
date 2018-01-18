from project import db
from project.models import BlogPost


# destroy the database
db.drop_all()

# create the database
db.create_all()

# insert
db.session.add(BlogPost("Good", "I\'m good."))
db.session.add(BlogPost("Well", "I\'m well."))
db.session.add(BlogPost("Hello", "Hello from the shell"))
db.session.add(BlogPost("Well", "Working with Postgres"))

# commit
db.session.commit()
