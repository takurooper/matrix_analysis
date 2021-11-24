import os

from flask import Flask

app = Flask(__name__)

@app.route("/")

def hello():
    return "Hello, world!!"

def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)