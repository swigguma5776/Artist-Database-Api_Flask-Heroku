from flask import Blueprint, render_template, request, redirect, url_for, flash 
from artist_inventory.models import User, db, check_password_hash
from artist_inventory.forms import UserLoginForm

# imports for flask_login
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    user_form = UserLoginForm()
    try:
        if request.method == 'POST' and user_form.validate_on_submit():
            first_name = user_form.first_name.data
            last_name = user_form.last_name.data
            email = user_form.email.data
            password = user_form.password.data
            print(first_name, last_name, email, password)

            user = User(first_name, last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account: {first_name} {last_name}", 'user-created')
    
            return redirect(url_for('site.home'))
    except:
        raise Exception ('Invalid Form Data: Please Check Your Form')
    
    
    return render_template('signup.html', user_form=user_form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    user_form = UserLoginForm()
    try:
        if request.method == 'POST' and user_form.validate_on_submit():
            first_name = user_form.first_name.data
            last_name = user_form.last_name.data
            email = user_form.email.data
            password = user_form.password.data
            print(first_name, last_name, email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: Via login information', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your login information is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', user_form=user_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))