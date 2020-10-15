import sys

import markdown

from flask import Flask, render_template, render_template_string
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask_flatpages import pygments_style_defs

def custom_renderer(template_str):
    markdown_text = render_template_string(template_str)
    pygmented_text = markdown.markdown(markdown_text, extensions=["codehilite", "fenced_code"])
    return pygmented_text

DEBUG = True

FLATPAGES_ROOT = "content"
FLATPAGES_EXTENSION = ".md"
FLATPAGES_HTML_RENDERER = custom_renderer

app = Flask(__name__)
app.config.from_object(__name__)

flat_pages = FlatPages(app)
freezer = Freezer(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/posts")
def posts():
    all_posts = (page for page in flat_pages if set(("date", "title")) <= page.meta.keys())
    sorted_posts = sorted(all_posts, key = lambda post: post.meta["date"], reverse=True)
    
    return render_template("posts.html", posts=sorted_posts)

@app.route("/posts/<post_name>")
def post(post_name):
    post = flat_pages.get_or_404(f"posts/{post_name}")
    return render_template("post.html", post=post)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=DEBUG)
