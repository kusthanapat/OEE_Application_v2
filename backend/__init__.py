from flask import Flask
from flask_bcrypt import Bcrypt
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.pardir, 'frontend', 'templates'),  # ../frontend/templates
    static_folder=os.path.join(os.path.pardir, 'frontend', 'static')       # ../frontend/static
)

app.config['SECRET_KEY'] = 'mysecret'

bcrypt = Bcrypt(app)
