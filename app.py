from flask import Flask, abort

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'
    abort(404)


if __name__ == '__main__':
    app.run()
