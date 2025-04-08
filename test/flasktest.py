from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return testlist

testlist = ['Hello', 'World', 'fish']

if __name__ == '__main__':
    app.run(debug=True)