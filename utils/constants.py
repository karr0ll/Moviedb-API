JWT_SECRET = "secret_word"
JWT_ALGORITHM = "HS256"
PWD_HASH_SALT = b"$eCr3t"
PWD_HASH_ITERATIONS = 100_000
AUTHORIZATIONS = {
        'JWT': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }