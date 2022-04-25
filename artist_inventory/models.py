from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   
import uuid  
from datetime import date, datetime 

# add security for passwords 
from werkzeug.security import generate_password_hash, check_password_hash

# import secrets module from python to get tokens
import secrets 

from flask_login import UserMixin

from flask_login import LoginManager 

from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow() 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = False,)
    last_name = db.Column(db.String(150), nullable = False,)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    artist = db.relationship('Artist', backref = 'owner', lazy = True)

    def __init__(self, first_name, last_name, email, id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash 

    def __repr__(self):
        return f"User {self.first_name} {self.last_name} has been added to the database"


class Artist(db.Model):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = False)
    last_name = db.Column(db.String(150), nullable = False)
    nationality = db.Column(db.String(150), nullable = False)
    art_period = db.Column(db.String(150), nullable = False)
    style = db.Column(db.String(150), nullable = False)
    most_famous_work = db.Column(db.String(150), nullable = False)
    scandals = db.Column(db.String(200), nullable = False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    # Changed some args to be default strings 

    def __init__(self, first_name, last_name, nationality, art_period, style, most_famous_work, scandals, user_token, id = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.art_period = art_period
        self.style = style
        self.most_famous_work = most_famous_work
        self.scandals = scandals
        self.user_token = user_token 

    def __repr__(self):
        return f"The following artist has been added: {self.first_name} {self.last_name}"

    def set_id(self):
        return (secrets.token_urlsafe())


# Create API Schema via Marshmallow Object
class ArtistSchema(ma.Schema):
    class Meta:
        fields = ['id', 'first_name', 'last_name','nationality','art_period',
        'style','most_famous_work','scandals','date_created']


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many = True)
