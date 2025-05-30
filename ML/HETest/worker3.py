import pandas as pd
import joblib
import numpy as np
from concrete.ml.sklearn import LinearSVC

import base64
from flask import Flask, request, jsonify

model = joblib.load("lsvc_concrete_model.pkl")
sample_input = np.load("sample_input.npy")
model.compile(sample_input)

app = Flask(__name__)

@app.route('/infer', methods=['POST'])
def infer():
    data = request.get_json()
    encrypted_batch = data.get("batch", [])

    results = []
    for enc_b64 in encrypted_batch:
        encrypted_input = model.fhe_circuit.encryptor.deserialize(base64.b64decode(enc_b64))
        encrypted_output = model.fhe_circuit.run(encrypted_input)
        serialized_result = base64.b64encode(encrypted_output.serialize()).decode("utf-8")
        results.append(serialized_result)

    return jsonify({"predictions": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
