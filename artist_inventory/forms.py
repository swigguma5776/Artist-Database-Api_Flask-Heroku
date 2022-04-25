from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from artist_inventory.models import db 

class UserLoginForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()


# Creating User Artist Form

class UserArtistForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()]) 
    nationality = StringField('Nationality', validators = [DataRequired()])
    art_period = StringField('Style', validators = [DataRequired()])
    style = StringField('Style', validators = [DataRequired()])
    most_famous_work = StringField('Style', validators = [DataRequired()])
    scandals = StringField('Style', validators = [DataRequired()])
    submit_button = SubmitField()

