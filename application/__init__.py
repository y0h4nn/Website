from flask import Flask


app = Flask(__name__)
app.debug = True
app.testing = True
app.secret_key = "Couscous la cle"


@app.route("/")
def root():
    return ""

