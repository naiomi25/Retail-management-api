from flask import Flask ,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app,origins="http://localhost:5173")


@app.route('/')
def inicializar():
    return ('LA API ESTÁ FUNCIONANDO')

@app.route("/api/hello")
def hello():
    return('te saludo desde mi backend')

if __name__ == "__main__":
    app.run(debug=True)