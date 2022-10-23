import os
import utils

from flask import Flask, jsonify, request, render_template, send_from_directory, redirect
from form import ShortenForm, AnaForm
from threading import Thread

app = Flask(__name__, template_folder="templates", static_url_path="")

app.config['SECRET_KEY'] = 'tgbaodeeptry'


@app.route('/<alias>', methods=['GET'])
def get_shortened(alias):
    if utils.db is not None and alias in utils.db:
        utils.db[f"c-{alias}"] += 1

        return redirect(utils.db[alias])
    else:
        return render_template("bad_url.html")


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory("", request.path[1:])


@app.route("/", methods=["GET", "POST"])
def home():
    form = ShortenForm()
    form2 = AnaForm()

    if request.method == "POST":
        if form.validate_on_submit():
            url = form.url.data

            if url[:4] != 'http':
                url = 'http://' + url

            if not utils.url_valid(url):
                return utils.bad_request('URL is not valid. Please try again')

            shortened_url = utils.shorten(url)
            utils.db[shortened_url] = url
            utils.db[f"c-{shortened_url}"] = 0

            return jsonify({
                'message':
                f"Your short URL is: <a href='/{shortened_url}' target='_blank' id='url-shortened'>"
                f"https://su.xbaotg.com/{shortened_url}"
                f"</a><br/>Your long URL is: <a href='{url}'>{url}</a>"
            }), 201

        elif form2.validate_on_submit():
            url = form2.code.data
            code = url.split("/")[-1]

            if len(code) != 6:
                return utils.bad_request("Your code is not exists")

            if utils.db is not None and f"c-{code}" in utils.db:
                return jsonify({
                    "message":
                    f"Your code is: {code}<br/>Count view is: {utils.db[f'c-{code}']}"
                }), 201
            else:
                return jsonify({"message": "Your link is not exists"}), 201

        return utils.bad_request("Please enter reCaptcha")

    return render_template("index.html", form=form, form2=form2)


@app.route('/assets/js/<path:path>')
def send_js(path):
    return send_from_directory('assets/js', path)


@app.route('/assets/css/<path:path>')
def send_css(path):
    return send_from_directory('assets/css', path)


@app.route('/assets/img/<path:path>')
def send_img(path):
    return send_from_directory('assets/img', path)


def run():
    app.run("0.0.0.0", port=5000, debug=True)


# t = Thread(target=run)
# t.start()
run()