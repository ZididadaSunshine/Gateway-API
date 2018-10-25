from app.main.config import secret


def decode_token(jwt):
    try:
        return jwt.decode(jwt, secret)['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
