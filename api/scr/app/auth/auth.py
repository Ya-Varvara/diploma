from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)


SECRET = "SECRET"
cookie_transport = CookieTransport(cookie_max_age=86400, cookie_name="cookie")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=86400)


auth_backend = AuthenticationBackend(
    name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy
)
