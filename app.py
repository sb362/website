import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True

FLATPAGES_EXTENSION = ".md"
FLATPAGES_ROOT = "content"

app = Flask(__name__)
app.config.from_object(__name__)

flat_pages = FlatPages(app)
freezer = Freezer(app)

@app.route("/")
def route_index():
    return render_template("index.html")

@app.route("/posts")
def route_posts():
    all_posts = (page for page in flat_pages if set(("date", "title")) <= page.meta.keys())
    sorted_posts = sorted(all_posts, key = lambda post: post.meta["date"], reverse=True)
    
    return render_template("posts.html", posts=sorted_posts)

@app.route("/posts/<post_name>")
def route_post(post_name):
    post = flat_pages.get_or_404(f"posts/{post_name}")
    return render_template("post.html", post=post)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=DEBUG)
