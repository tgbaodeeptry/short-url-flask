from flask import Flask, jsonify, request, render_template, send_from_directory
from form import ShortenForm
import utils
from threading import Thread


app = Flask(__name__, template_folder="templates", static_url_path="")
app.config['SECRET_KEY'] = 'tgbaodeeptry'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdWLT0cAAAAAKaoWbrrzYn8NJg5JjlrYRe9mE_-'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdWLT0cAAAAAGnirpAYmn9DDb5CoC8_-rfxBRX_'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}


@app.route('/<alias>', methods=['GET'])
def get_shortened(alias):
    if utils.db is not None and alias in utils.db:
        return render_template("redirect.html", url=utils.db[alias])

    else:
        return render_template("bad_url.html")


@app.route("/", methods=["GET", "POST"])
def home():
    form = ShortenForm(csrf_enabled=True)

    if request.method == "POST":
        if form.validate_on_submit():
            url = form.url.data

            if url[:4] != 'http':
                url = 'http://' + url

            if not utils.url_valid(url):
                return utils.bad_request('URL is not valid. Please try again')

            shortened_url = utils.shorten(url)
            utils.db[shortened_url] = url

            return jsonify({'message': f"Your short URL is: <a href='/{shortened_url}' target='_blank'>"
                                       f"https://su.tgbao.me/{shortened_url}"
                                       f"</a><p></p>Your long URL is: <a href='{url}'>{url}</a>"}), 201

        return jsonify({"message": "Unknown error. Try again"})

    return render_template("index.html", form=form)


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
    app.run("0.0.0.0", port=5000)


t = Thread(target=run)
t.start()