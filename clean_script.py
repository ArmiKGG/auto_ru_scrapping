from flask import Flask, render_template, redirect, url_for, flash, abort, request, json
from flask_bootstrap import Bootstrap
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'saasfasfasf'
Bootstrap(app)


@app.route('/')
def gome():
    return render_template("index.html")


@app.route('/naeb', methods=["GET", "POST"])
def home():
    link = request.args.get('link')
    soupped = soup_it(link)
    auto_ru = AutoRu(soupped[0], soupped[1])
    comment = auto_ru.get_comment()
    tag = auto_ru.get_tag()
    specs = auto_ru.get_specs()
    return render_template("car.html", comment=comment, tag=tag, specs=specs)


if __name__ == "__main__":
    app.run(debug=True)
