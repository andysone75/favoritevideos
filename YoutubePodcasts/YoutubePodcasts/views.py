from datetime import datetime
from flask import render_template, request, redirect
from YoutubePodcasts import app, youtube, db
from YoutubePodcasts.models import Users, Videos
from YoutubePodcasts.login import *
import flask_login
import hashlib

@app.route('/')
@app.route('/home')
def home():
    if flask_login.current_user.is_anonymous:
        return redirect('/login')

    if flask_login.current_user.is_anonymous:
        title = 'Youtube Podcasts'
    else:
        title = flask_login.current_user.id

    videos = Videos.query.filter_by(username=flask_login.current_user.id).all()

    return render_template(
        'yp2/index.html',
        title='Favorite Videos',
        user_name=flask_login.current_user.id,
        videos=videos,
        bg_video_url='static/home/video/nvidia-rtx.mp4')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_page_error = render_template(
        'yp2/login.html',
        title='FV - Login',
        error_message='Wrong username or password')

    if request.method == 'GET':
        return render_template(
            'yp2/login.html',
            title='FV - Login')

    username = request.form['username']
    record = Users.query.filter_by(username=username).first()

    if record is None:
        return login_page_error

    if hashlib.sha256(request.form['password'].encode()).hexdigest() == record.password:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect('/')

    return login_page_error

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/login')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if flask_login.current_user.is_anonymous:
        return redirect('/login')

    link = None
    if request.method == 'POST' and 'link' in request.form:
        link = request.form['link']
        video_info = youtube.download_info(link)
        db.session.add(Videos(
            flask_login.current_user.id,
            link, 
            video_info['title'], 
            video_info['uploader'],
            video_info['uploader_url'],
            video_info['thumbnail']))
        db.session.commit()
        return redirect("/")

    return render_template(
        'yp2/add.html',
        title='FV - videos')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template(
            'yp2/signup.html',
            title='FV - Signup')
    login = request.form['username']
    password = request.form['password']
    if login and password:
        if Users.query.filter_by(username=login).first() is not None:
            return render_template(
                'yp2/signup.html',
                title = 'VF - Signup',
                error_message='This name is taken. Come up with another')
        Users.create(Users(login, hashlib.sha256(password.encode()).hexdigest()))
        user = User()
        user.id = login
        flask_login.login_user(user)
        print(f'New user created: {login}')
    return redirect('/')

