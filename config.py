import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SYS_MAIL_SUBJECT_PREFIX = '[红外热像分析系统]'
    SYS_MAIL_SENDER = 'Administrator <ahu_confirm@163.com>'

#    UPLOADED_NOCOIMAGES_DEST = '/root/no_co_images'
#    UPLOADED_COIMAGES_DEST = '/root/co_images_diagnose_images'
#    UPLOADED_ORIGINALIMAGES_DEST = '/root/co_images_original_images'
#    UPLOADED_CLEANIMAGES_DEST = '/root/co_images_clean_images'
#    UPLOADED_CCDIMAGES_DEST = '/root/co_images_ccd_images'
#    UPLOADED_MATRIXTEMP_DEST = '/root/co_images_matrix_temp'

    UPLOADED_NOCOIMAGES_DEST = '/Users/abnerwang/Documents/no_co_images'
    UPLOADED_COIMAGES_DEST = '/Users/abnerwang/Documents/co_images_diagnose_images'
    UPLOADED_ORIGINALIMAGES_DEST = '/Users/abnerwang/Documents/co_images_original_images'
    UPLOADED_CLEANIMAGES_DEST = '/Users/abnerwang/Documents/co_images_clean_images'
    UPLOADED_CCDIMAGES_DEST = '/Users/abnerwang/Documents/co_images_ccd_images'
    UPLOADED_MATRIXTEMP_DEST = '/Users/abnerwang/Documents/co_images_matrix_temp'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                              'mysql://root:wxp12345@localhost/temp_detect_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                              'mysql://root:wxp12345@localhost/temp_detect_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                              'mysql://root:wxp12345@localhost/temp_detect'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
