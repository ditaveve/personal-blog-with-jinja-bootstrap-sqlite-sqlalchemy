# Personal Blog with Jinja, Bootstrap, SQLAlchemy & Flask-Login

🔗 Live at: [https://personal-blog-with-jinja-bootstrap.onrender.com/](https://personal-blog-with-jinja-bootstrap.onrender.com/)

Days 57/59/60/67/69 of my 100 Days of Code Python challenge. This started as the Blog Capstone project: on Day 57 the goal was pulling data from an API and rendering it dynamically with Jinja, on Day 59 the styling was upgraded using the Bootstrap "Clean Blog" theme, on Day 60 the "Contact Page" became active and working, on Day 67 it grew into a full CRUD blog backed by a real database, and on Day 69 it became a proper multi-user site — accounts, admin privileges, and a comment system.

## What it does

A Flask blog backed by SQLite (via Flask-SQLAlchemy). Anyone can browse posts and read them; registered users can leave comments; only the admin account can create, edit, or delete posts. Posts and comments are both written with a rich-text editor (CKEditor) rather than plain text, and there's a working contact form that emails you directly.

## Features

- **Public blog** — homepage lists every post; each post has its own page.
- **Accounts** — register, log in, log out. Passwords are hashed (never stored or compared as plain text).
- **Comments** — logged-in users can comment on any post. Each comment shows the commenter's name and a Gravatar avatar, generated from an MD5 hash of their email.
- **Admin privileges** — only the admin account can create, edit, or delete posts. This is enforced server-side with a custom `@admin_only` decorator, not just hidden buttons in the UI — so a non-admin can't get around it by visiting the URL directly either.
- **Contact form** — sends an email via Gmail SMTP.

## Tech stack

- [Flask](https://flask.palletsprojects.com/)
- Jinja2 templating, with shared `header.html`/`footer.html` partials
- [Bootstrap-Flask](https://bootstrap-flask.readthedocs.io/) (Bootstrap 5) for styling and form rendering
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) / SQLAlchemy 2.0 — typed `Mapped`/`mapped_column` models with real one-to-many relationships (`User` → `BlogPost`, `User` → `Comment`, `BlogPost` → `Comment`)
- SQLite
- [Flask-Login](https://flask-login.readthedocs.io/) — sessions, `current_user`, `@login_required`
- [Flask-WTF](https://flask-wtf.readthedocs.io/) / [WTForms](https://wtforms.readthedocs.io/) — CSRF protection and form validation on every form
- [Flask-CKEditor](https://flask-ckeditor.readthedocs.io/) — rich text for both posts and comments
- Werkzeug's `generate_password_hash` / `check_password_hash` for password storage
- Gravatar, via `hashlib.md5` of the user's email, for avatars

## Security notes

- Passwords are hashed with `pbkdf2:sha256` before ever touching the database — the raw password is never stored or logged.
- Every form (register, login, new/edit post, comment, contact) goes through Flask-WTF, which includes CSRF token protection automatically.
- Admin-only actions are gated at the route level (`@admin_only`), so protection doesn't rely on the frontend hiding buttons — direct requests to `/new-post`, `/edit-post/<id>`, or `/delete/<id>` are rejected with a 403 for anyone who isn't the admin.
- `SECRET_KEY` is loaded from an environment variable (`.env`), not hardcoded in the source.

## Routes

| Route                      | Method(s)   | Description                                        |
| ---------------------------- | ------------ | ----------------------------------------------------- |
| `/`                           | GET          | Homepage — lists all posts                           |
| `/post/<int:num>`             | GET, POST    | View a post; submit a comment (must be logged in)     |
| `/register`                   | GET, POST    | Create an account                                     |
| `/login`                      | GET, POST    | Log in                                                |
| `/logout`                     | GET          | Log out (requires being logged in)                    |
| `/new-post`                   | GET, POST    | Create a new post (admin only)                        |
| `/edit-post/<post_id>`        | GET, POST    | Edit an existing post, pre-filled (admin only)         |
| `/delete/<post_id>`           | GET, DELETE  | Delete a post (admin only)                            |
| `/about`                      | GET          | About page                                            |
| `/contact`                    | GET, POST    | Contact form, sends an email via Gmail SMTP           |

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
