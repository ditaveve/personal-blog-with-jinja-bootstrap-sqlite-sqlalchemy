from flask import Flask, render_template, url_for
import requests
import os


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

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
