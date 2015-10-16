from flask import Flask                      # type: ignore

from config import CONFIG_DICT

app = Flask(__name__)
app.config.update(CONFIG_DICT)