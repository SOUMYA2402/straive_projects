from flask import Flask, request, jsonify
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array(data["features"]).reshape(1, -1)  # [Age, Salary]
    prediction = int(model.predict(features)[0])
    return jsonify({"HighIncome": prediction})

if __name__ == "__main__":
    app.run()