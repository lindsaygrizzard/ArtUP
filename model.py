"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

import os


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    project_name = db.Column(db.String(64), nullable=True, default='Project')
    project_disc = db.Column(db.String(64), nullable=True, default='My Project')

    def __repr__(self):

        """Provide helpful representation when printed"""

        return "<Project project_id: %s | user_id: %s | project_name: %s>" % (
               self.project_id, self.user_id, self.project_name)


class Wall(db.Model):

    """Virtual 'wall' for calculating horizontal margins"""

    __tablename__ = "walls"

    wall_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    wall_name = db.Column(db.String(64), nullable=True, default='Wall')
    wall_width = db.Column(db.Integer, nullable=False)
    wall_height = db.Column(db.Integer, nullable=False)
    center_line = db.Column(db.Integer, default=58, nullable=True)
    wall_img = db.Column(db.String(200), nullable=True)
    offset_percent = db.Column(db.String(64), default=3000, nullable=True)
    wall_disc = db.Column(db.String(64), nullable=True, default='My Wall')

    def __repr__(self):

        """Provide helpful representation when printed"""

        return "<Wall wall_id: %s | project_id: %s | wall_name: %s>" % (
               self.wall_id, self.project_id, self.wall_name)


class Wall_Art(db.Model):

    """Reference table to allow multiple artwork id's on several wall iterations"""

    __tablename__ = "walls_art"

    wall_art_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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
    wall_id = db.Column(db.Integer, db.ForeignKey('walls.wall_id'))
    art_name = db.Column(db.String, nullable=True, default='Stock Artwork')
    device_code = db.Column(db.String, nullable=False, default='none')
    art_height = db.Column(db.Integer, nullable=False)
    art_width = db.Column(db.Integer, nullable=False)
    device_distance = db.Column(db.Integer, default=0, nullable=True)
    art_img = db.Column(db.String(200), nullable=True)

    def __repr__(self):

        """Provide helpful representation when printed"""
        return "<Art art_id: %s | art_name: %s>" % (
               self.art_id, self.art_name)


###########################################################################
#Helper Functions

def connect_to_db(app):
    """Connect the database to our Flask app."""
    DATABASE_URL = os.environ.get("DATABASE_URL",
                              'postgresql://localhost/artup')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

