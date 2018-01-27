from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads, TEXT

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
no_co_images = UploadSet('NoCoImages', IMAGES)
co_images = UploadSet('CoImages', IMAGES)
original_images = UploadSet('OriginalImages', IMAGES)
clean_images = UploadSet('CleanImages', IMAGES)
ccd_images = UploadSet('CCDImages', IMAGES)
matrix_temp = UploadSet('MatrixTemp', TEXT)

login_manager = LoginManager()
login_manager.session_protection = 'Strong'  # 防止用户会话遭篡改
login_manager.login_view = 'auth.login'  # 设置登录端点


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    configure_uploads(app, no_co_images)
    configure_uploads(app, co_images)
    configure_uploads(app, original_images)
    configure_uploads(app, clean_images)
    configure_uploads(app, ccd_images)
    configure_uploads(app, matrix_temp)

    # 注册 main 蓝本（用于邮件发送的账户确认）
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册用户认证蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 注册上传图片蓝本
    from .upload_image import upload_image as upload_image_blueprint
    app.register_blueprint(upload_image_blueprint, url_prefix='/upload')

    # 注册图片查询蓝本
    from .query_image import query_image as query_image_blueprint
    app.register_blueprint(query_image_blueprint, url_prefix='/query')

    return app
