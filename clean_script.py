import random

from flask import Flask, render_template, redirect, url_for, flash, abort, request, json
from flask_bootstrap import Bootstrap
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'saasfasfasf'
Bootstrap(app)




@app.route('/', methods=["GET", "POST"])
def home():
    data = requests.post('https://hotel.dev.expoforum.ru/api/get_guests', params={
        "hotel_id": "admin"
    },
                         headers={
        'X-API-KEY': 'cboFMpzoOFBmYd9G0RGaLpp35jhi4LKtGedflM1WD5WDWyTceIxJFMxLcbFJtM6y'
    }).json()
    try:
        return render_template("car.html", data=data)
    except Exception as e:
        return print(f"Lox OSHIBKU POYMAL - {e}")


@app.route('/pdf', methods=["GET", "POST"])
def pdf():
    if request.method == 'GET':
        return render_template('pdf.html')
    req_id = request.form.get('req_id')
    file = request.files['file']
    d = requests.post('https://hotel.dev.expoforum.ru/api/update/pdf', data={
        "req_id": req_id,
        "new_status": 1
    },
                  files={'file_bytes': file}
                      )
    return d.json()


@app.route('/link', methods=["GET", "POST"])
def link():
    if request.method == 'GET':
        return render_template('link.html')
    req_id = request.form.get('req_id')
    link = request.form.get('link')
    d = requests.post('https://hotel.dev.expoforum.ru/api/update/url', data={
        "req_id": req_id,
        "new_status": 1,
        "link": link,
    })
    return d.json()


@app.route('/decline', methods=["GET", "POST"])
def decline():
    if request.method == 'GET':
        return render_template('decline.html')
    req_id = request.form.get('req_id')
    d = requests.post('https://hotel.dev.expoforum.ru/api/update/decline', data={
        "req_id": req_id,
        "new_status": -1,
    })
    return d.json()


if __name__ == "__main__":
    app.run(debug=True)
