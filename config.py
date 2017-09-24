import os
here = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    配置基类
    """
    SECRET_KEY = '#+^aOjdlPHFD09)&*2P3JR-0CFE)&H12EAa;OPFG=0'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN = 'chenjiandongx@qq.com'
    FLASK_POSTS_PER_PAGE = 15
    MAIL_USE_SSL = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SENDER = '简微博团队<chenjiandongx@qq.com>'
    FLASK_MAIL_SUBJECT_PREFIX = '[简微博]'


class DevelopmentConfig(Config):
    """
    开发状态
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'data-dev.sqlite')


class TestingEmptyConfig(Config):
    """
    测试状态：数据库无数据
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'data-test-empty.sqlite')


class TestingFullConfig(Config):
    """
    测试状态：数据库有数据
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'data-test-full.sqlite')


class ProductionConfig(Config):
    """
    生产状态
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'data-prod.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing-empty': TestingEmptyConfig,
    'testing-full': TestingFullConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
