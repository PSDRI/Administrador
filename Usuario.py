import jwt
import datetime

class Auth:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)  
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return "Token expirado. Faça login novamente."
        except jwt.InvalidTokenError:
            return "Token inválido. Faça login novamente."


if __name__ == "__main__":

    auth = Auth('GAP')
    user_id = 135012
    token = auth.create_token(user_id)
    print(f"Token gerado: {token}")

    user = auth.verify_token(token)
    if isinstance(user, int):
        print(f"Usuário autenticado: {user}")
    else:
        print(f"Erro de autenticação: {user}")
