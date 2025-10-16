# from flask import Flask
# app=Flask(__name__)
# @app.route('/<name>')
# def print_hello(name):
#     return f"hello {name}"
#
# if __name__=='__main__':
#     app.run()


#calculator#

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Calculator with route parameters!"

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    return jsonify(operation="addition", a=a, b=b, result=a + b)

@app.route('/subtract/<int:a>/<int:b>')
def subtract(a, b):
    return jsonify(operation="subtraction", a=a, b=b, result=a - b)

@app.route('/multiply/<int:a>/<int:b>')
def multiply(a, b):
    return jsonify(operation="multiplication", a=a, b=b, result=a * b)

@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    if b == 0:
        return jsonify(error="Division by zero is not allowed"), 400
    return jsonify(operation="division", a=a, b=b, result=a / b)

if __name__ == '__main__':
    app.run(debug=True)
