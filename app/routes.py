from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Meeting
from datetime import datetime
from flask_moment import Moment


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/book', methods=['GET', 'POST'])
def book():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    date = str(datetime.utcnow())
    meetings = Meeting.query.filter(Moment(Meeting.date).isAfter(date))
    arrayStart = [None]
    arrayEnd = [None]
    arrayOwner = [None]
    arrayOComment = [None]
    arrayCComment = [None]
    if meetings is not None:
        for entries in meetings:
            arrayDate += meetings.date
            arrayStart += meetings.time_start
            arrayEnd += meetings.time_end
            #client = meetings.client_id
            arrayOComment += meetings.manager_comment
            arrayCComment += meetings.client_comment
        return render_template('book.html', title='Book', arrayStart=arrayStart, arrayEnd=arrayEnd, arrayOComment=arrayOComment, arrayCComment=arrayCComment)
    else:
        return render_template('book.html', title='Book')
    if form.validate_on_submit():
        starttime = form.starttime.data
        endtime = form.endtime.data
        date = form.date.data
        ownerComment = form.oComment.data
        clientComment = form.cComment.data
        meeting = Meeting(date=date, time_start=starttime, time_end=endtime, client_comment=clientComment, owner_comment=ownerComment)
        db.session.add(meeting)
        db.session.commit()
