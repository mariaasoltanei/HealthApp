from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64

app = Flask(__name__)

# Load AES key from file
with open("aes_key.txt", "r") as f:
    base64_key = f.read().strip()

AES_KEY = base64.b64decode(base64_key)

def decrypt_value(encrypted_b64, iv_b64):
    encrypted = base64.b64decode(encrypted_b64)
    iv = base64.b64decode(iv_b64)
    aesgcm = AESGCM(AES_KEY)
    decrypted_bytes = aesgcm.decrypt(iv, encrypted, None)
    return float(decrypted_bytes.decode("utf-8"))  # Return float value of x/y/z

@app.route("/sensorData", methods=["POST"])
def process():
    try:
        payload = request.get_json()
        data_items = payload.get("data", [])
        context = payload.get("context", {})

        decrypted_batch = []

        for item in data_items:
            try:
                decrypted_item = {
                    "sensorType": item["sensorType"],
                    "timestamp": item["timestamp"],
                    "userId": item["userId"],
                    "x": decrypt_value(item["x"], item["ivX"]),
                    "y": decrypt_value(item["y"], item["ivY"]),
                    "z": decrypt_value(item["z"], item["ivZ"])
                }
                decrypted_batch.append(decrypted_item)

            except Exception as entry_error:
                print(f"❌ Failed to decrypt item: {entry_error}")

        return jsonify({
            "status": "success",
            "decrypted_count": len(decrypted_batch),
            "first_decrypted_item": decrypted_batch[0] if decrypted_batch else None
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route("/test", methods=["GET"])
def test():
    print("Test endpoint hit.")
    return {"status": "success"}, 200
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)