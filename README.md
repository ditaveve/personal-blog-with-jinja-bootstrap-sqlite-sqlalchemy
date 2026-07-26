# Blog Capstone

Day 57 of my [100 Days of Code](https://www.100daysofcode.com/) journey. This is the first part of the Blog Capstone project, where the goal was to get comfortable pulling data from an API and rendering it dynamically with Jinja templates in Flask.

## What it does

A tiny Flask app that fetches a list of blog posts from a remote API and displays them on a homepage. Click "Read" on any post and it takes you to a dedicated page for that post.

## What I practiced

- Setting up routes in Flask, including dynamic routes with URL parameters (`/post/<int:num>`)
- Fetching JSON data from an external API with `requests`
- Looping over data in a template with Jinja's `{% for %}` and using `loop.index0` to know which post you're on
- Passing that index through `url_for()` to build the link to each post's page

## Running it

```bash
pip install flask requests
python main.py
```

Then open `http://127.0.0.1:5000/` in your browser.
