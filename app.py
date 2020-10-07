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
def index():
    return render_template("index.html")

@app.route("/posts")
def posts():
    return render_template("posts.html", posts=flat_pages)

@app.route("/posts/<post_name>")
def post(post_name):
    post_page = flat_pages.get_or_404(f"posts/{post_name}")
    return render_template("post.html", post=post_page)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=DEBUG)
