import unittest

from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing-empty')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """ 测试实例已经启动
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """ 测试使用`TESTING-EMPTY`配置
        """
        self.assertTrue(current_app.config['TESTING'])
