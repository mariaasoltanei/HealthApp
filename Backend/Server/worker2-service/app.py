from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Dummy logic: randomly decide "fall_detected" or "no_fall"
    prediction = random.choice(["walking", "standing", "sitting"])

    # Dummy logic: generate random confidence between 0.7 and 1.0
    confidence = round(random.uniform(0.7, 1.0), 2)

    return jsonify({
        "prediction": prediction,
        "confidence": confidence
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
