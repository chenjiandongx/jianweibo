import os
here = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '#+^aOjdlPHFD09)&*2P3JR-0CFE)&H12EAa;OPFG=0'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True        # 每次关闭会话都保存提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False      # 数据库变化追踪
    FLASK_ADMIN = 'chenjiandongx@qq.com'        # 管理员邮箱


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_USE_SSL = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    FLASK_MAIL_SENDER = '简微博团队'
    FLASK_MAIL_SUBJECT_PREFIX = '[简微博]'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'data.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
