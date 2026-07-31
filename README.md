# Personal Blog with Jinja and Bootstrap

Days 57/59/60 of my [100 Days of Code](https://www.100daysofcode.com/) journey. This is the Blog Capstone project: on Day 57 the goal was to get comfortable pulling data from an API and rendering it dynamically with Jinja templates in Flask, on Day 59 the styling was upgraded using the Bootstrap "Clean Blog" theme and on Day 60 the "Contact Page" became active and working.

## What it does

A tiny Flask app that fetches a list of blog posts from a remote API and displays them on a homepage, styled with Bootstrap. Click a post and it takes you to a dedicated page for that post.

## What I practiced

- Setting up routes in Flask, including dynamic routes with URL parameters (`/post/<int:num>`)
- Fetching JSON data from an external API with `requests`
- Looping over data in a template with Jinja's `{% for %}` and using `loop.index0` to know which post you're on
- Passing that index through `url_for()` to build the link to each post's page
- Styling the site with Bootstrap and a shared `header.html`/`footer.html` layout included across pages
- Using `url_for('static', ...)` for CSS, JS, and images so links resolve correctly regardless of the current route

## Running it

```bash
pip install flask requests
python main.py
```

Then open `http://127.0.0.1:5000/` in your browser.
