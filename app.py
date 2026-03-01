from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Привет! Это минимальное приложение для демонстрации Jenkins 🎉</h1>"

@app.route('/status')
def status():
    return jsonify({"status": "ok", "message": "Приложение работает"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
