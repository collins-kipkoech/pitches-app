from .. import db,photos
from app.models import User,Pitch
from flask import flash, redirect, render_template, url_for,request
from flask_login import current_user, login_user, logout_user,login_required

from . import auth
from .forms import EditProfileForm, LoginForm, RegistrationForm
from ..email import mail_message


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    # import pdb; pdb.set_trace() 
    if form.validate_on_submit():
        print('work')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        mail_message("Welcome to PicthesHub","email/welcome_user",user.email,user=user)

        return redirect(url_for('.login'))
    return render_template("registration/register.html", title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('registration/login.html', title='Sign In', form=form)
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))    
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    pitches=Pitch.query.filter_by(user=current_user.id)
    # import pdb; pdb.set_trace()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        current_user.profile_pic_path = path
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('registration/profile.html', title='Edit Profile',
                           form=form,pitches=pitches)    
