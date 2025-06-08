from flask import Flask
from flask_session import Session

app = Flask(__name__)

from src.routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, use_reloader = True)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)