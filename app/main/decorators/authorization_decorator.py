from functools import wraps

from app.main.model.invalid_token_model import InvalidToken
from app.main.service.authorization_service import get_token, decode_token, AuthorizationResponse


def require_authorization(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_token()

        if token:
            # Check that token is valid
            invalid_token = InvalidToken.query.filter_by(token=token).first()
            if not invalid_token:
                decoded_token = decode_token(token)

                if decoded_token:
                    return func(*args, **kwargs)

        # Either no token was provided or it is invalid. Either way, return an unauthorized response
        return dict(message='You are not authorized to perform this request.'), AuthorizationResponse.Unauthorized

    return decorated
