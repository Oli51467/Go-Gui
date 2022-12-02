from sqlalchemy import create_engine


class DevelopmentConfig:
    REQUEST_IP = 'http://127.0.0.1:5000/'


class ProductionConfig:
    REQUEST_IP = 'http://8.142.10.225:5001/'

    HOSTNAME = '8.142.10.225'
    DATABASE = 'gorobot'
    DB_PORT = 3306
    USERNAME = 'goRobot'
    PASSWORD = 'Hmis1234.'
    DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, DB_PORT, DATABASE)
    engine = create_engine(DB_URL)


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
