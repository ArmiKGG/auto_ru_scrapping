from flask import Flask, render_template, redirect, url_for, flash, abort, request, json
from flask_bootstrap import Bootstrap
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'saasfasfasf'
Bootstrap(app)


@app.route('/')
def gome():
    return render_template("index.html")


@app.route('/naeb_na_dalari', methods=["GET", "POST"])
def home():
    link = request.args.get('link')
    soupped = soup_it(link)
    auto_ru = AutoRu(soupped[0], soupped[1])
    comment = auto_ru.get_comment()
    tag = auto_ru.get_tag()
    specs = auto_ru.get_specs()
    params_second = auto_ru.get_params()
    images_second = specs[1]
    images_first = auto_ru.get_images()
    try:
        return render_template("car.html", comment=comment, tag=tag, specs=specs[0], images_s=images_second, params_s=params_second, images_f=images_first)
    except Exception as e:
        return print(f"Lox OSHIBKU POYMAL - {e}")


if __name__ == "__main__":
    app.run(debug=True)
