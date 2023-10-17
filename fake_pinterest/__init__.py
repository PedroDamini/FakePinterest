from flask import Flask


app = Flask(__name__)

from fake_pinterest import routes