from base64 import b64encode
from hashlib import blake2b
import random
import re
from replit import db

from flask import Flask, jsonify, request, render_template, send_from_directory


app = Flask(__name__, template_folder="templates", static_url_path="")


def url_valid(url):
    return re.match(regex, url) is not None


def shorten(url):
    url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    while url_hash in db:
        url += str(random.randint(0, 9))
        url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)

    b64 = b64encode(url_hash.digest(), altchars=b'-_')
    return b64.decode('utf-8')


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    url = request.values.get("url", "")

    if url[:4] != 'http':
        url = 'http://' + url

    if not url_valid(url):
        return bad_request('Provided url is not valid.')

    shortened_url = shorten(url)
    db[shortened_url] = url

    return jsonify({'message': f"Your short URL is: <a href='/{shortened_url}' target='_blank'>"
                               f"https://su.tgbao.me/{shortened_url}"
                               f"</a><p></p>Your long URL is: <a href='{url}'>{url}</a>"}), 201


@app.route('/<alias>', methods=['GET'])
def get_shortened(alias):
    if db is not None and alias in db:
        return render_template("redirect.html", url=db[alias])

    else:
        return render_template("bad_url.html")


regex = re.compile(
    r'^(?:http)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

DIGEST_SIZE = 6

# -------------------------------


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route('/assets/js/<path:path>')
def send_js(path):
    return send_from_directory('assets/js', path)


@app.route('/assets/css/<path:path>')
def send_css(path):
    return send_from_directory('assets/css', path)


@app.route('/assets/img/<path:path>')
def send_img(path):
    return send_from_directory('assets/img', path)


if __name__ == '__main__':
    app.run(debug=True)
