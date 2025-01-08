from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Dados recebidos:", data)

    return jsonify({"message": "Evento processado"}), 200


if __name__ == "__main__":
    app.run(port=5000)
