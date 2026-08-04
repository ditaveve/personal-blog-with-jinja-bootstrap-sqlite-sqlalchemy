from flask import Flask, render_template, url_for, request, jsonify, redirect
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



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str]
    date: Mapped[str]
    body: Mapped[str]
    author: Mapped[str]
    img_url: Mapped[str]
    subtitle: Mapped[str]

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        
        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Name of the author', validators=[DataRequired()])
    img_url = StringField('Background Image URL', validators=[DataRequired(),  URL(require_tld=True, message="Must be a valid URL")])
    body = CKEditorField('The body of the post', validators=[DataRequired()])
    submit = SubmitField('Submit Post')

@app.route('/', methods=['GET'])
def home():
    if request.method == "GET":
        posts = db.session.execute(db.select(BlogPost)).scalars().all()
        return render_template("index.html", posts=posts)


@app.route('/post/<int:num>', methods=['GET'])
def get_article(num):
    if request.method == "GET":
        posts = db.session.execute(db.select(BlogPost)).scalars().all()
        return render_template("post.html", post=posts[num])

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
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        newpost = BlogPost(
            title = form.title.data,
            date = datetime.datetime.now().strftime("%B %d, %Y"),
            subtitle = form.subtitle.data,
            author = form.author.data,
            img_url = form.img_url.data,
            body = form.body.data
        )
        db.session.add(newpost)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('make-post.html', form=form, ok=True)

@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalars().all()[0]
    edit_form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.date = datetime.datetime.now().strftime("%B %d, %Y")
        post.subtitle = edit_form.subtitle.data
        post.author = edit_form.author.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('make-post.html', form=edit_form, ok=False)

@app.route('/delete/<post_id>', methods=['GET', 'DELETE'])
def delete(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
