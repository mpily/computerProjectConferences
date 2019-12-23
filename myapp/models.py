from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from myapp import db, login_manager

class Conference(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'conferences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60) )
    description = db.Column(db.String(200))
    startdate = db.Column(db.Date,unique=True)
    enddate = db.Column(db.Date,unique=True)
    registrationClosed = db.Column(db.Boolean,default=False)


    def __repr__(self):
        return  self.name

class Workshop(db.Model):
    """Create a Workshop table"""
    __tablename__= 'workshops'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(200))
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    duration = db.Column(db.Interval)
    conference_id= db.Column(db.Integer, db.ForeignKey('conferences.id',ondelete='CASCADE'))

    def __repr__(self):
        return self.description



class Participant(UserMixin,db.Model):
    """create a  Participant table"""
    __tablename__='participants'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),)
    email= db.Column(db.String(60),unique=True)
    password_hash=db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Participant: {}>'.format(self.name)

    # Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Participant.query.get(int(user_id))


class Attend(db.Model):
    """create a view for the attendees workshop"""
    __tablename__= 'attendees'
    email= db.Column(db.String(60),db.ForeignKey('participants.email',ondelete='CASCADE'),primary_key=True)
    Workshhop_id= db.Column(db.Integer,db.ForeignKey('workshops.id',ondelete='CASCADE'),primary_key=True)

class Room(db.Model):
    ''' create a table forr the rooms that will be used '''
    __tablename__='rooms'
    room_number=db.Column(db.Integer,primary_key=True)
    floor_number=db.Column(db.Integer,primary_key=True)
    capacity = db.Column(db.Integer,primary_key=True)

class Event(db.Model):
    ''' create a view for the events that will give us the room  workshop and number of people attending'''
    __tablename__='events'
    room_number=db.Column(db.Integer,db.ForeignKey('rooms.room_number'),primary_key=True)
    floor_number=db.Column(db.Integer,db.ForeignKey('rooms.floor_number'),primary_key=True)
    workshop_id=db.Column(db.Integer,db.ForeignKey('workshops.id'),primary_key=True,unique=True)
    workshopname=db.Column(db.String(60))
    participants=db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    def __repr__(self):
        return self.workshopname
