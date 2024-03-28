from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/drivers')
def drivers():
    return ["driver1", "driver2"]

@app.route('/add_driver/<driver>')
def add_driver(driver):
    return driver

if __name__ == '__main__':
    app.run()
