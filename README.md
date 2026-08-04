# Personal Blog with Jinja, Bootstrap & Flask-SQLAlchemy

Days 57/59/60/67 of my [100 Days of Code](https://www.100daysofcode.com/) journey. This started as the Blog Capstone project: on Day 57 the goal was pulling data from an API and rendering it dynamically with Jinja, on Day 59 the styling was upgraded using the Bootstrap "Clean Blog" theme, on Day 60 the "Contact Page" became active and working, and on Day 67 it grew into a full CRUD blog — posts now live in a database instead of a remote API, and I added RESTful routes to create, edit, and delete them.

## What it does

A Flask blog backed by SQLite (via Flask-SQLAlchemy). The homepage lists all posts; clicking one opens its full page. Posts are written with a rich-text editor (CKEditor) rather than plain text, and there's a working contact form that emails you directly. No login/auth yet — anyone hitting `/new-post` can currently create a post.

## Routes

| Route                      | Method(s)   | Description                                  |
| ---------------------------- | ------------ | ----------------------------------------------- |
| `/`                           | GET          | Homepage — lists all posts                     |
| `/post/<int:num>`             | GET          | View a single post                             |
| `/new-post`                   | GET, POST    | Form to create a new post                      |
| `/edit-post/<post_id>`        | GET, POST    | Form to edit an existing post, pre-filled       |
| `/delete/<post_id>`           | GET, DELETE  | Deletes a post                                 |
| `/about`                      | GET          | About page                                     |
| `/contact`                    | GET, POST    | Contact form, sends an email via Gmail SMTP     |

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your email credentials for the contact form:

```
MY_EMAIL=your_email@gmail.com
MY_EMAIL_PASSWORD=your_gmail_app_password
```

## Running it

```bash
python main.py
```

Then open `http://127.0.0.1:5001/` in your browser.
