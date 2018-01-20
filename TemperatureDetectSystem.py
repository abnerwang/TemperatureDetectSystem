import os

import pymysql
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

from app import create_app, db
from app.models import User, NoCoImage, CoImage

pymysql.install_as_MySQLdb()
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, NoCoImage=NoCoImage, CoImage=CoImage)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
# HTTPS 暂不实现
# manager.add_command('runserver', Server('localhost', port=443, ssl_crt="app/cert.pem", ssl_key="app/key.pem"))
manager.add_command('runserver', Server('localhost', port=8080))

if __name__ == '__main__':
    manager.run()
