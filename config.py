import time

import os


class Config:
    SECRET_KEY = 'Wxp%^&*#sdhaklfhkjdsai3s234@$$+;'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'ahu_confirm@163.com'
    MAIL_PASSWORD = 'wxp12345'
    SYS_MAIL_SUBJECT_PREFIX = '[红外热像分析系统]'
    SYS_MAIL_SENDER = 'Administrator <ahu_confirm@163.com>'

    NOCOIMAGES_DEST_PRE = '/home/abnerwang/no_co_images'
    COIMAGES_DEST_PRE = '/home/abnerwang/diagnose_images'
    ORIGINALIMAGES_DEST_PRE = '/home/abnerwang/original_images'
    CLEANIMAGES_DEST_PRE = '/home/abnerwang/clean_images'
    CCDIMAGES_DEST_PRE = '/home/abnerwang/ccd_images'
    MATRIXTEMP_DEST_PRE = '/home/abnerwang/matrix_temp'

    # NOCOIMAGES_DEST_PRE = '/Users/abnerwang/Documents/no_co_images'
    # COIMAGES_DEST_PRE = '/Users/abnerwang/Documents/diagnose_images'
    # ORIGINALIMAGES_DEST_PRE = '/Users/abnerwang/Documents/original_images'
    # CLEANIMAGES_DEST_PRE = '/Users/abnerwang/Documents/clean_images'
    # CCDIMAGES_DEST_PRE = '/Users/abnerwang/Documents/ccd_images'
    # MATRIXTEMP_DEST_PRE = '/Users/abnerwang/Documents/matrix_temp'

    year = time.strftime('%Y', time.localtime(time.time()))
    month = time.strftime('%m', time.localtime(time.time()))

    no_co_images_dest = NOCOIMAGES_DEST_PRE + '/' + year + '/' + month
    co_images_dest = COIMAGES_DEST_PRE + '/' + year + '/' + month
    original_images_dest = ORIGINALIMAGES_DEST_PRE + '/' + year + '/' + month
    clean_images_dest = CLEANIMAGES_DEST_PRE + '/' + year + '/' + month
    ccd_images_dest = CCDIMAGES_DEST_PRE + '/' + year + '/' + month
    matrix_temp_dest = MATRIXTEMP_DEST_PRE + '/' + year + '/' + month

    if not os.path.exists(no_co_images_dest):
        os.makedirs(no_co_images_dest)
    if not os.path.exists(co_images_dest):
        os.makedirs(co_images_dest)
    if not os.path.exists(original_images_dest):
        os.makedirs(original_images_dest)
    if not os.path.exists(clean_images_dest):
        os.makedirs(clean_images_dest)
    if not os.path.exists(ccd_images_dest):
        os.makedirs(ccd_images_dest)
    if not os.path.exists(matrix_temp_dest):
        os.makedirs(matrix_temp_dest)

    UPLOADED_NOCOIMAGES_DEST = no_co_images_dest
    UPLOADED_COIMAGES_DEST = co_images_dest
    UPLOADED_ORIGINALIMAGES_DEST = original_images_dest
    UPLOADED_CLEANIMAGES_DEST = clean_images_dest
    UPLOADED_CCDIMAGES_DEST = ccd_images_dest
    UPLOADED_MATRIXTEMP_DEST = matrix_temp_dest

    # UPLOADED_NOCOIMAGES_DEST = '/Users/abnerwang/Documents/no_co_images'
    # UPLOADED_COIMAGES_DEST = '/Users/abnerwang/Documents/co_images_diagnose_images'
    # UPLOADED_ORIGINALIMAGES_DEST = '/Users/abnerwang/Documents/co_images_original_images'
    # UPLOADED_CLEANIMAGES_DEST = '/Users/abnerwang/Documents/co_images_clean_images'
    # UPLOADED_CCDIMAGES_DEST = '/Users/abnerwang/Documents/co_images_ccd_images'
    # UPLOADED_MATRIXTEMP_DEST = '/Users/abnerwang/Documents/matrix_temp'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                              'mysql://abnerwang:Wxp#1991&0910@localhost/temp_detect_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                              'mysql://abnerwang:Wxp#1991&0910@localhost/temp_detect_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                              'mysql://abnerwang:Wxp#1991&0910@localhost/temp_detect'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
