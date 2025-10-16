# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flasgger import Swagger
# from sklearn.linear_model import LogisticRegression
# import numpy as np
#
# app = Flask(__name__)
# # Use SQLite instead of MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# swagger = Swagger(app)
#
# # -----------------
# # Database model
# # -----------------
# class Customer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     age = db.Column(db.Integer)
#     balance = db.Column(db.Float)
#
# with app.app_context():
#     db.create_all()
#
# # -----------------
# # CRUD APIs
# # -----------------
# @app.route('/customer', methods=['POST'])
# def add_customer():
#     data = request.get_json()
#     new_customer = Customer(name=data['name'], age=data['age'], balance=data['balance'])
#     db.session.add(new_customer)
#     db.session.commit()
#     return jsonify({'message': 'Customer added successfully'}), 200
#
# @app.route('/customers', methods=['GET'])
# def get_customers():
#     customers = Customer.query.all()
#     result = [{'id': c.id, 'name': c.name, 'age': c.age, 'balance': c.balance} for c in customers]
#     return jsonify(result)
#
# @app.route('/customer/<int:id>', methods=['PUT'])
# def update_customer(id):
#     data = request.get_json()
#     customer = Customer.query.get(id)
#     if not customer:
#         return jsonify({'error': 'Customer not found'}), 404
#     customer.name = data.get('name', customer.name)
#     customer.age = data.get('age', customer.age)
#     customer.balance = data.get('balance', customer.balance)
#     db.session.commit()
#     return jsonify({'message': 'Customer updated successfully'})
#
# @app.route('/customer/<int:id>', methods=['DELETE'])
# def delete_customer(id):
#     customer = Customer.query.get(id)
#     if not customer:
#         return jsonify({'error': 'Customer not found'}), 404
#     db.session.delete(customer)
#     db.session.commit()
#     return jsonify({'message': 'Customer deleted successfully'})
#
# # -----------------
# # ML Model Training & Prediction
# # -----------------
# @app.route('/train', methods=['POST'])
# def train_model():
#     X = np.array([[25, 2000], [40, 6000], [50, 8000], [30, 3000]])
#     y = np.array([0, 1, 1, 0])  # 0=low, 1=high income
#
#     global model
#     model = LogisticRegression()
#     model.fit(X, y)
#     return jsonify({'message': 'Model trained successfully'})
#
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     features = np.array([[data['age'], data['balance']]])
#     prediction = model.predict(features)[0]
#     return jsonify({'prediction': int(prediction)})
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sklearn.linear_model import LogisticRegression
import numpy as np

app = Flask(__name__)
# Use SQLite instead of MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
swagger = Swagger(app)

# -----------------
# Database model
# -----------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    balance = db.Column(db.Float)

with app.app_context():
    db.create_all()

# -----------------
# CRUD APIs
# -----------------
@app.route('/customer', methods=['POST'])
def add_customer():
    """
    Add a new customer
    ---
    tags:
      - Customer
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - age
            - balance
          properties:
            name:
              type: string
              example: John Doe
            age:
              type: integer
              example: 30
            balance:
              type: number
              example: 5000.0
    responses:
      200:
        description: Customer added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Customer added successfully
    """
    data = request.get_json()
    new_customer = Customer(name=data['name'], age=data['age'], balance=data['balance'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 200

@app.route('/customers', methods=['GET'])
def get_customers():
    """
    Get all customers
    ---
    tags:
      - Customer
    responses:
      200:
        description: List of customers
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Jane Smith
              age:
                type: integer
                example: 35
              balance:
                type: number
                example: 7000.0
    """
    customers = Customer.query.all()
    result = [{'id': c.id, 'name': c.name, 'age': c.age, 'balance': c.balance} for c in customers]
    return jsonify(result)

@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    """
    Update a customer by ID
    ---
    tags:
      - Customer
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Customer ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Updated Name
            age:
              type: integer
              example: 40
            balance:
              type: number
              example: 10000.0
    responses:
      200:
        description: Customer updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Customer updated successfully
      404:
        description: Customer not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: Customer not found
    """
    data = request.get_json()
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    customer.name = data.get('name', customer.name)
    customer.age = data.get('age', customer.age)
    customer.balance = data.get('balance', customer.balance)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """
    Delete a customer by ID
    ---
    tags:
      - Customer
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Customer ID
    responses:
      200:
        description: Customer deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Customer deleted successfully
      404:
        description: Customer not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: Customer not found
    """
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

# -----------------
# ML Model Training & Prediction
# -----------------
@app.route('/train', methods=['POST'])
def train_model():
    """
    Train the logistic regression model
    ---
    tags:
      - ML Model
    responses:
      200:
        description: Model trained successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Model trained successfully
    """
    X = np.array([[25, 2000], [40, 6000], [50, 8000], [30, 3000]])
    y = np.array([0, 1, 1, 0])  # 0=Loan Not approved, 1=Loan Approved

    global model
    model = LogisticRegression()
    model.fit(X, y)
    return jsonify({'message': 'Model trained successfully'})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict income category based on age and balance
    ---
    tags:
      - ML Model
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - age
            - balance
          properties:
            age:
              type: integer
              example: 35
            balance:
              type: number
              example: 4000.0
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            prediction:
              type: integer
              description: 0=low income, 1=high income
              example: 1
    """
    data = request.get_json()
    features = np.array([[data['age'], data['balance']]])
    try:
        prediction = model.predict(features)[0]
    except NameError:
        return jsonify({'error': 'Model not trained yet. Please train the model first by calling /train'}), 400
    return jsonify({'prediction': int(prediction)})



@app.route('/trainloan', methods=['POST'])
def train_modelloan():
    """
    Train the logistic regression model
    ---
    tags:
      - ML Model
    responses:
      200:
        description: Model trained successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Model trained successfully
    """
    X = np.array([[25, 2000], [40, 6000], [50, 8000], [30, 3000]])
    y = np.array([0, 1, 1, 0])  # 0=low, 1=high income

    global model
    model = LogisticRegression()
    model.fit(X, y)
    return jsonify({'message': 'Model trained successfully'})

@app.route('/predictloan', methods=['POST'])
def predictloan():
    """
    Predict income category based on age and balance
    ---
    tags:
      - ML Model
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - age
            - balance
          properties:
            age:
              type: integer
              example: 35
            balance:
              type: number
              example: 4000.0
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            prediction:
              type: integer
              description: 0=low income, 1=high income
              example: 1
    """
    data = request.get_json()
    features = np.array([[data['age'], data['balance']]])
    try:
        prediction = model.predict(features)[0]
    except NameError:
        return jsonify({'error': 'Model not trained yet. Please train the model first by calling /train'}), 400
    return jsonify({'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)
