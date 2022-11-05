class Config(object):
    SECRET_KEY = 'my-super-secret-key'
    JWT_SECRET_KEY = 'my-super-secret-key'
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    JWT_REFRESH_COOKIE_PATH = '/api/refreshToken'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:toor@localhost/calibri'
    CORS_ORIGINS = '*'
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


client_id = 1033434944741052516
client_secret = 'tIGzApafGjosJz7qKInjMKFpN0-pTTVJ'
redirect_uri = 'http://80.78.251.233:3000/login'
logs_secret = 'super_secret'
