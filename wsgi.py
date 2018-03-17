import pymysql

from app import create_app

pymysql.install_as_MySQLdb()
application = create_app('production')

if __name__ == '__main__':
    application.run()
