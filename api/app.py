from flask import Flask, request, jsonify
from auth import authenticate, requires_auth, create_user
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
    try:
        db.write_batch(data)
        return jsonify({'status': 'success'})
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/read', methods=['POST'])
@requires_auth
def read():
    keys = request.json.get('keys')
    if not keys:
        return jsonify({'error': 'No keys provided'}), 400
    data = db.read_batch(keys)
    return jsonify({'data': data})

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    if create_user(data['username'], data['password']):
        return jsonify({'status': 'User created successfully'})
    return jsonify({'error': 'User already exists'}), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)