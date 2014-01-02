# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, mail
from forms import SignupForm, LoginForm, EditForm, PostForm, CommentForm
from models import User, Post, Comment, Registration, ROLE_STUDENT, ROLE_ADMIN, CATEGORY_NEWS, CATEGORY_NOTES, CATEGORY_QUESTIONS, CATEGORY_STREAM
from datetime import datetime
from emails import send_email
from config import ADMINS
from hashlib import md5
import re


"""
    Strona główna - tu wyświetlane są aktualności
"""
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/strona/<int:page>', methods = ['GET', 'POST'])
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.body.data,
                    short = re.sub('<[A-Za-z\/][^>]*>', '', form.body.data), 
                    title = form.title.data,
                    thumbnail_link = form.picture.data, 
                    timestamp = datetime.utcnow(),
                    category = CATEGORY_NEWS,
                    author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Dodano post')
        return redirect(url_for('index'))

    posts = Post.query.filter_by(category=CATEGORY_NEWS).order_by(Post.id.desc()).paginate(page, 5, False)

    return render_template("index.html",
                           user = g.user,
                           posts = posts,
                           form = form)

"""
    Obsługa rejestracji
"""
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        nick = form.username.data
        us = User.query.filter_by(nickname = nick).first()
        print us
        if us is None:
            pass_hash = md5(form.password.data).hexdigest()
            send_email(subject=u'Założenie konta na Candeli',
                    sender = 'grzegorz.parka',
                    recipients = [form.email.data],
                    text_body = render_template('account_creation_mail.txt', 
                                                nick = nick,
                                                password_hash = pass_hash),
                    html_body = render_template('account_creation_mail.html',
                                                nick = nick,
                                                password_hash = pass_hash))
            flash(u"""Wysłaliśmy Ci maila z linkiem aktywacyjnym.
            Sprawdź swoją skrzynkę wydziałową :)""")
            pending_user = Registration(nickname = form.username.data,
                                        password = unicode(pass_hash),
                                        email = form.email.data,
                                        salt = 'a')
            db.session.add(pending_user)
            db.session.commit()
        else:
            flash(u"""Nie możesz wybrać tej nazwy użytkownika. 
                    Użytkownik już istnieje.""")

    nickname = request.args.get("username")
    password = request.args.get("pass")

    if nickname and password:
        pending_user = Registration.query.filter_by(nickname = nickname).first()
        if pending_user.password == password:
            flash(u"""Witaj na Candeli! Teraz zaloguj się używając wybranej
                        przy rejestracji nazwy użytkownika oraz hasła.""")
            user = User(nickname = nickname,
                        password = unicode(password),
                        email = pending_user.email)
            db.session.add(user)
            db.session.delete(pending_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash(u"""Niewłaściwe dane użytkownika.""") 
    return render_template('signup.html',
                            title = u'Zarejestruj się',
                            form = form)

"""
    Obsługa logowania
"""
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname = form.username.data).first()
        if user is not None and md5(form.password.data).hexdigest() == user.password:
            login_user(user, remember = form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash(u"""Nieprawidłowe dane logowania.""")
    return render_template('login.html',
                           title = u'Zaloguj się',
                           form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/profile/<nickname>')
@login_required
def profile(nickname):
    user = User.query.filter_by(nickname = nickname).first_or_404()
    posts = Post.query.filter_by(user_id = user.id).limit(5)
    return render_template('user.html',
                           user = user,
                           posts = posts)


@app.route('/edit_profile', methods =['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Zmiany zapisane.')
        return redirect(url_for('edit_profile'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form = form)


@app.route('/notes', methods =['GET', 'POST'])
@login_required
def notes():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.body.data, 
                    short = form.body.data[:200], 
                    title = form.title.data,
                    thumbnail_link = form.picture.data, 
                    timestamp = datetime.utcnow(),
                    category = CATEGORY_NOTES,
                    author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Dodano post')
        return redirect(url_for('notes'))

    posts = Post.query.filter_by(category=CATEGORY_NOTES).order_by(Post.id.desc())

    return render_template("notes.html",
                           user = g.user,
                           posts = posts,
                           form = form)

@app.route('/questions', methods =['GET', 'POST'])
@login_required
def questions():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.body.data,
                    short = form.body.data[:200],  
                    title = form.title.data,
                    thumbnail_link = form.picture.data, 
                    timestamp = datetime.utcnow(),
                    category = CATEGORY_QUESTIONS,
                    author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Dodano post')
        return redirect(url_for('questions'))

    posts = Post.query.filter_by(category=CATEGORY_QUESTIONS).order_by(Post.id.desc())

    return render_template("questions.html",
                           user = g.user,
                           posts = posts,
                           form = form)

@app.route('/stream', methods =['GET', 'POST'])
@login_required
def stream():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.body.data,
                    short = form.body.data[:200], 
                    title = form.title.data,
                    thumbnail_link = form.picture.data, 
                    timestamp = datetime.utcnow(),
                    category = CATEGORY_STREAM,
                    author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Dodano post')
        return redirect(url_for('stream'))

    posts = Post.query.filter_by(category=CATEGORY_STREAM).order_by(Post.id.desc())

    return render_template("stream.html",
                           user = g.user,
                           posts = posts,
                           form = form)

@app.route('/detail/<int:post_id>',  methods = ['GET', 'POST'])
@login_required
def detail(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body = form.text.data, 
                    post_id = post_id,
                    timestamp = datetime.utcnow(),
                    author = g.user)
        db.session.add(comment)
        db.session.commit()
        flash('Dodano komentarz.')
        """return redirect(url_for('detail/<post_id>'))"""

    post = Post.query.filter_by(id = post_id).first_or_404()
    comments = Comment.query.filter_by(post_id = post_id).all()

    return render_template("detail.html",
                            user = g.user,
                            comments = comments,
                            post = post,
                            form = form)

@app.route('/delete/<int:id>', methods = ['GET'])
@login_required
def delete(id):
    content_type = request.args.get("content_type")
    if content_type == "post":
        post = Post.query.get_or_404(id)
        if post.author.id != g.user.id:
            flash(u'Nie możesz usunąć tego posta.')
            return redirect(url_for('index'))
        db.session.delete(post)
        db.session.commit()
        flash(u'Post usunięty.')
    elif content_type == "comment":
        comment = Comment.query.get_or_404(id)
        if comment.author.id != g.user.id:
            flash(u'Nie możesz usunąć tego komentarza.')
            return redirect(url_for('index'))
        db.session.delete(comment)
        db.session.commit()
        flash(u'Komentarz usunięty.')
    else:
        redirect(url_for('404'))
    return redirect(url_for('index'))

@app.route('/statistics')
@login_required
def statistics():
    users = User.query.all()
    return render_template("statistics.html", users = users)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/terms_of_usage')
def terms_of_usage():
    return render_template("terms.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
