import os
class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProdConfig(Config):

    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:colo1234@localhost/pitch'


config_options ={
    'production': ProdConfig,
    'development':DevConfig
}
