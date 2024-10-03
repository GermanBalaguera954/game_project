from flask import Flask, jsonify, request

app = Flask(__name__)

# Ruta simple para probar la API
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from the backend!'})

if __name__ == '__main__':
    app.run(debug=True)