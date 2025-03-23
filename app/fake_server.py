from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "RoboTrader V1.8 está rodando na nuvem 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
