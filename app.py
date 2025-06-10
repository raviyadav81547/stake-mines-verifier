
from flask import Flask, request, jsonify, render_template
import hashlib, hmac, random

app = Flask(__name__)

def generate_board(server_seed, client_seed, nonce, mines):
    combined = f"{server_seed}:{client_seed}:{nonce}"
    hash_bytes = hmac.new(server_seed.encode(), combined.encode(), hashlib.sha256).digest()
    random.seed(hash_bytes)
    positions = list(range(25))
    random.shuffle(positions)
    mine_positions = sorted(positions[:mines])
    board = ['💣' if i in mine_positions else '🟩' for i in range(25)]
    return board

@app.route("/", methods=["GET", "POST"])
def index():
    board = None
    if request.method == "POST":
        server_seed = request.form["server_seed"]
        client_seed = request.form["client_seed"]
        nonce = int(request.form["nonce"])
        mines = int(request.form["mines"])
        board = generate_board(server_seed, client_seed, nonce, mines)
    return render_template("index.html", board=board)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
