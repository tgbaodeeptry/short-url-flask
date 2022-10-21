from flask_wtf import Form, RecaptchaField
from wtforms.fields.html5 import URLField
from wtforms.validators import url


class ShortenForm(Form):
    url = URLField(validators=[url()])
    recaptcha = RecaptchaField()
