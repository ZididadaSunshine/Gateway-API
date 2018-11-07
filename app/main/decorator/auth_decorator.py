from app.main.service.authorization_service import is_authorized, get_token


def auth_required(api):
    def wrapper(func):
        def check_auth(*args, **kwargs):
            if not is_authorized(get_token()):
                api.abort(403)

            return func(*args, **kwargs)

        return check_auth

    return wrapper
