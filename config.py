class DevelopmentConfig:
    REQUEST_IP = 'http://127.0.0.1:5000/'


class ProductionConfig:
    REQUEST_IP = 'http://8.142.10.225:5001/'


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
