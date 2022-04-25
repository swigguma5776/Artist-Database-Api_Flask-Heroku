from flask import Blueprint, render_template, request, redirect, url_for, flash #added request, redirect, url_for, & flash
from flask_login.utils import login_required

from artist_inventory.models import Artist, User, db  #added db & User
from flask_login import current_user
from artist_inventory.forms import UserArtistForm # added UserArtistForm


"""
Note that in the code below,
some arguments are specified when creating the Blueprint object.
First argument, "site", is the Blueprint name,
used by Flask routing mechanism. #site = Routing 

Second argument, __name__, is Blueprint's import name,
which Flask uses to locate Blueprint's resources. #__name__ = Resources
"""

site = Blueprint('site', __name__, template_folder ='site_templates')

@site.route('/')
def home(): 
    return render_template('index.html')


# @site.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html')




# Creating User Created Artist Route

@site.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    artist_form = UserArtistForm()
    print(artist_form.errors)
    print('hello')
    try:
        if request.method == 'POST' and artist_form.validate_on_submit():
            print('hello again')
            first_name = artist_form.first_name.data
            last_name = artist_form.last_name.data
            nationality = artist_form.nationality.data
            art_period = artist_form.art_period.data
            style = artist_form.style.data
            most_famous_work = artist_form.most_famous_work.data
            scandals = artist_form.scandals.data
            user_token = current_user.token
            print(first_name, last_name, nationality, art_period, style, most_famous_work, scandals)

            artist = Artist(first_name, last_name, nationality, art_period, style, most_famous_work, scandals, user_token=user_token)

            db.session.add(artist)
            db.session.commit()

            flash(f"You have successfully created a new artist: {first_name} {last_name}", 'artist-created')
    
            return redirect(url_for('site.profile'))
        else:
            print('else')
    except:
        raise Exception ('Invalid Form Data: Please Check Your Form')
    
    # artists = Artist.query.filter_by(user_token = current_user.token).all()
    
    return render_template('create.html', artist_form=artist_form)
    


@site.route('/profile')
@login_required
def profile():
    artists = Artist.query.filter_by(user_token = current_user.token).all()
    return render_template('profile.html', artists=artists)