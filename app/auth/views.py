from . import auth
from flask import render_template,redirect,url_for,flash
from .forms import RegistrationForm,LoginForm
from app import db
from flask_login import current_user, login_user,logout_user
from app.models import User

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