import pandas as pd
import joblib
import numpy as np
from concrete.ml.sklearn import LinearSVC

import base64
from flask import Flask, request, jsonify
from concrete.ml.deployment import FHEModelServer

fhemodel_server = FHEModelServer("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model")  # path to compiled model directory

app = Flask(__name__)

@app.route('/infer', methods=['POST'])
def infer():
    try:
        encrypted_batch = request.get_json()["batch"]
        print(f"Received batch of size: {len(encrypted_batch)}")
        # print(encrypted_batch)
        results = []
        with open("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model"+ "/serialized_evaluation_keys.ekl", "rb") as f:
            serialized_evaluation_keys = f.read()
        for enc_b64 in encrypted_batch:
            print(f"Processing encrypted input: {enc_b64}")
            print("-------------")
            encrypted_bytes = base64.b64decode(enc_b64)
            print(f"Decoded encrypted input: {encrypted_bytes}")
            encrypted_result = fhemodel_server.run(encrypted_bytes, serialized_evaluation_keys)
            results.append(base64.b64encode(encrypted_result).decode("utf-8"))
        return jsonify({"predictions": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)  # Run the server on port 5002
