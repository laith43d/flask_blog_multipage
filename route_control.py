from datetime import date
from flask import render_template, request
from passlib.hash import sha256_crypt
from helpers import *
from models import db, Users, Articles, Comments
from forms import RegisterForm, ArticleForm, CommentForm
from config import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    if fetched_articles := Articles.query.all():
        return render_template('articles.html', articles = fetched_articles)

    return render_template('articles.html')


@app.route('/article/<article_id>', methods = ['GET', 'POST'])
def article(article_id):
    candidate_article = Articles.query.filter_by(id = article_id).first()
    displayed_comments = Comments.query.filter_by(article_id = article_id)
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate_comment = Comments(
            author = Users.query.filter_by(username = session['username']).first().name,
            article_id = article_id,
            comment = form.comment.data,
            created_date = date.today()
        )
        db.session.add(candidate_comment)
        db.session.commit()
        return redirect(url_for('articles'))
    if candidate_article:
        return render_template('article.html', article = candidate_article, comments = displayed_comments, form = form)
    flash("Article not found", 'danger')
    return redirect(url_for('articles'))


@app.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users(
            name = form.name.data,
            email = form.email.data,
            username = form.username.data,
            password = sha256_crypt.hash(str(form.password.data)),
            register_date = date.today()
        )
        db.session.add(user)
        db.session.commit()

        flash('You are now registered.', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form = form)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        # fetch the form data without wtf form
        username = request.form['username']
        password_candidate = request.form['password']
        queried_user = Users.query.filter_by(username = username).first()

        if queried_user and sha256_crypt.verify(password_candidate, queried_user.password):
            app.logger.info('PASSED')
            session['logged_in'] = True
            session['username'] = queried_user.username
            flash('You are now logged in', 'success')
            return redirect(url_for("dashboard"))
        else:
            error = 'Username or password is not correct'
            return render_template('login.html', error = error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    if fetched_articles := Articles.query.all():
        return render_template('dashboard.html', articles = fetched_articles)

    return render_template('dashboard.html')


@app.route('/add_article', methods = ['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate_article = Articles(
            title = form.title.data,
            author = Users.query.filter_by(username = session['username']).first().name,
            body = form.body.data,
            created_date = date.today()
        )
        db.session.add(candidate_article)
        db.session.commit()
        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form = form)


@app.route('/edit_article/<string:editable_id>', methods = ['GET', 'POST'])
@login_required
def edit_article(editable_id):
    editable_article = Articles.query.filter_by(id = editable_id).first()
    form = ArticleForm(request.form)

    form.title.data = editable_article.title
    form.body.data = editable_article.body

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        Articles.query.filter_by(id = editable_id).update({'title': title, 'body': body})
        db.session.commit()
        flash("Article Updated", "success")
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form = form)


@app.route('/delete_article/<string:article_id>', methods = ['POST'])
@login_required
def delete_article(article_id):
    Comments.query.filter_by(article_id = article_id).delete()
    Articles.query.filter_by(id = article_id).delete()
    db.session.commit()

    flash("Article deleted", 'success')
    return redirect(url_for('dashboard'))

