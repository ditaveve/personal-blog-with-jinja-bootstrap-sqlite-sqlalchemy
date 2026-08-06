from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, abort
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import requests
import os
import smtplib
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from hashlib import md5

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_KEY")
Bootstrap5(app)
ckeditor = CKEditor(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI", "sqlite:///posts.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class BlogPost(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str]
    date: Mapped[str]
    body: Mapped[str]
    #author: Mapped[str]
    img_url: Mapped[str]
    subtitle: Mapped[str]

    author_id = db.Column(db.Integer, db.ForeignKey("users.id")) #the link between dbs
    author: Mapped["User"] = relationship(back_populates="posts") #some shortcut, lets you
                                                        #write some_post.author and get back 
                                                        # the actual User object
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    avatar: Mapped[str]

    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str]
    date: Mapped[str]

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["BlogPost"] = relationship(back_populates="comments")

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

def admin_only(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if (not current_user.is_authenticated) or (current_user.id != 1):
            abort(403)
        return func(*args, **kwargs)
    return wrapper_func

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    img_url = StringField('Background Image URL', validators=[DataRequired(),  URL(require_tld=True, message="Must be a valid URL")])
    body = CKEditorField('The body of the post', validators=[DataRequired()])
    submit = SubmitField('Submit Post')

@app.route('/', methods=['GET'])
def home():
    if request.method == "GET":
        posts = db.session.execute(db.select(BlogPost)).scalars().all()
        return render_template("index.html", posts=posts)


@app.route('/post/<int:num>', methods=['GET', 'POST'])
def get_article(num):
    comment_form = CommentForm()
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    if comment_form.validate_on_submit():
        try:
            new_comment = Comment(
                content=comment_form.content.data, 
                date = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p"), 
                author=current_user, 
                post=posts[num]
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('get_article', num=num))
        except AttributeError:
            flash("You need to be logged in to comment on this post.")
            return redirect(url_for('login'))
    return render_template("post.html", post=posts[num], form=comment_form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        MY_EMAIL = os.getenv('MY_EMAIL')
        MY_EMAIL_PASSWORD = os.getenv('MY_EMAIL_PASSWORD')
        final_message = (
            f"Subject: New contact form message from {name}\n\n"
            f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        )

        connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=final_message)
        
        return render_template('contact.html', ok=0)
    except Exception:
        return render_template('contact.html', ok=1)

@app.route('/form-entry', methods=['GET', 'POST'])
def receive_data():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    print(name)
    print(email)
    print(phone)
    print(message)
    return render_template('contact')

@app.route('/new-post', methods=['GET', 'POST'])
@admin_only
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        newpost = BlogPost(
            title = form.title.data,
            date = datetime.datetime.now().strftime("%B %d, %Y"),
            subtitle = form.subtitle.data,
            img_url = form.img_url.data,
            body = form.body.data,
            author = current_user
        )
        db.session.add(newpost)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('make-post.html', form=form, ok=True)

@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
@admin_only
def edit_post(post_id):
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalars().all()[0]
    edit_form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.date = datetime.datetime.now().strftime("%B %d, %Y")
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('make-post.html', form=edit_form, ok=False)

@app.route('/delete/<post_id>', methods=['GET', 'DELETE'])
@admin_only
def delete(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if request.method == "POST" and register_form.validate_on_submit():
        user = User(
            name = register_form.name.data,
            email = register_form.email.data,
            password = generate_password_hash(password=register_form.password.data, method="pbkdf2:sha256", salt_length=8),
            avatar = 'https://www.gravatar.com/avatar/' + md5(register_form.email.data.encode('utf-8')).hexdigest()
        )
        existing_user = db.session.execute(db.select(User).where(User.email==user.email)).scalars().all()
        if existing_user:
            flash("You've already signed up with that email. Log in instead.")
            return redirect(url_for('login'))
        
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('home'))
    return render_template("register.html", form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == "POST" and login_form.validate_on_submit():
        user = User(
            email = login_form.email.data,
            password = login_form.password.data
        )
        existing_user = db.session.execute(db.select(User).where(User.email==user.email)).scalars().all()
        if (not existing_user) or ( not check_password_hash(existing_user[0].password, user.password) ):
            flash("The email/password is incorrect. Try again.")
            return redirect(url_for('login'))
        else:
            login_user(existing_user[0])
            return redirect(url_for('home'))
    return render_template('login.html', form=login_form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=False, port=5001)
