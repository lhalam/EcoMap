from flask import Flask

ecomap = Flask(__name__)


@ecomap.route('/')
def index():
    return "<h1>Apache works!!!</h1>"


if __name__ == "__main__":
    ecomap.run()
