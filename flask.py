from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GAP'  
users = {
    'admin': 'senha_admin',
   
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token de autenticação ausente!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token de autenticação inválido!'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Falha na autenticação!'}), 401

    if auth.username in users and users[auth.username] == auth.password:
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'message': 'Falha na autenticação!'}), 401

@app.route('/admin', methods=['GET'])
@token_required
def admin():
    return jsonify({'message': 'Protegida para administradores.'})

if __name__ == '__main__':
    app.run(debug=True)
