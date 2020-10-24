class Config:
    pass


class ProdConfig:

    pass

class DevConfig:
    pass


config_options ={
    'production': ProdConfig,
    'development':DevConfig
}
