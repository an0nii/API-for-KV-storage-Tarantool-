from flask import Flask, request, jsonify
from auth import authenticate, requires_auth
from database import TarantoolDB

app = Flask(__name__)
db = TarantoolDB()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    token = authenticate(data['username'], data['password'])
    if token:
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/write', methods=['POST'])
@requires_auth
def write():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    db.write_batch(data)
    return jsonify({'status': 'success'})

@app.route('/api/read', methods=['POST'])
@requires_auth
def read():
    keys = request.json.get('keys')
    if not keys:
        return jsonify({'error': 'No keys provided'}), 400
    data = db.read_batch(keys)
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)