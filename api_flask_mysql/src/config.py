class DevelopmentConfig():
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MYSQL_DB = 'miproyecto'

config = {
    'development' : DevelopmentConfig
}