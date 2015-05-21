"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy() 

#######################################################################
#Model definitions

class User(db.Model):
	"""User of Art Installation website"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	zipcode = db.Column(db.String(15), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed"""

		return "<User user_id:  %s | email: %s>" % (self.user_id, self.email)




class Project(db.Model):
	"""Project 'folder' for user to group multiple walls"""

	__tablename__ = "projects"

	project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),) #nullable?? 
	project_name = db.Column(db.String(64), nullable=True, default='Project')

	def __repr__(self):
		"""Provide helpful representation when printed"""

		return "<Project project_id: %s | user_id: %s | project_name: %s>" % (
									self.project_id, self.user_id, self.project_name)




class Wall(db.Model):
	"""Virtual 'wall' for calculating horizontal margins"""

	__tablename__ = "walls"

	wall_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id')) #nullable??
	wall_name = db.Column(db.String(64), nullable=True, default='Wall')  
	wall_width = db.Column(db.Integer, nullable=False) #will multiple x 1000
	center_line = db.Column(db.Integer, default=58, nullable=True) #nullable for future customization | #will multiple x 1000
	wall_img = db.Column(db.String(200), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed"""

		return "<Wall wall_id: %s | project_id: %s | wall_name: %s>" % (
												self.wall_id, self.project_id, self.wall_name)




class Wall_Art(db.Model):
	"""Reference table to allow multiple artwork id's on several wall iterations"""

	__tablename__ = "walls_art"

	wall_art_id = db.Column(db.Integer, autoincrement=True, primary_key=True) #necessary???
	wall_id = db.Column(db.Integer, db.ForeignKey('walls.wall_id')) 
	art_id = db.Column(db.Integer, db.ForeignKey('arts.art_id'), nullable=False) 

	def __repr__(self):
		"""Provide helpful representation when printed"""
		return "<Wall wall_art_id: %s | wall_id: %s | art_id: %s>" % (
									self.wall_art_id, self.wall_id, self.art_id)


class Art(db.Model):
	"""Data for individual dimensions of specific art pieces (calculating 
		longitudinal margins)"""

	__tablename__ = "arts"

	art_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	art_name = db.Column(db.String, nullable=True, default='Stock Artwork') 
	device_code = db.Column(db.String, db.ForeignKey('devices.device_code'))
	# wall_id = db.Coluzmn(db.Integer, db.ForeignKey('walls.wall_id')) 
	height = db.Column(db.Integer, nullable=False) #will multiple x 1000
	width = db.Column(db.Integer, nullable=False) #will multiple x 1000
	device_distance = db.Column(db.Integer, nullable=True, default=0) 
	art_img = db.Column(db.String(200), nullable=True)

	def __repr__(self):
		"""Provide helpful representation when printed"""
		return "<Art art_id: %s | art_name: %s>" % (
										self.art_id, self.art_name)
   

class Hang_Device(db.Model): #RENAME TO 'DEVICE'
	"""Specifics for type of hanging devices for artworks 
	and measurement from device to top of piece"""

	__tablename__ = "devices"

	#'1' , '2', corners, cleat
	
	device_code = db.Column(db.String, primary_key=True) 

	def __repr__(self):
		"""Provide helpful representation when printed"""

		return "<Device device_code : %s>" % (self.device_code)

###########################################################################
#Helper Functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artup.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."







