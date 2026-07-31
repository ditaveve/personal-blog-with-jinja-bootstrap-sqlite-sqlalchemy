from flask import Flask, render_template, url_for, request
import requests
import os
import smtplib
from dotenv import load_dotenv


app = Flask(__name__)

@app.route('/')
def home():
    blog_url = "https://api.npoint.io/e51cef75bd4706884a78"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("index.html", posts=all_posts)

@app.route('/post/<int:num>')
def get_article(num):
    blog_url = "https://api.npoint.io/e51cef75bd4706884a78"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("post.html", post=all_posts[num])

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


if __name__ == "__main__":
    app.run(debug=True, port=5001)
