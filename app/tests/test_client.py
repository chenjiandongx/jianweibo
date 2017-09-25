import unittest

from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing-empty')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.update_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """ 测试首页
        """
        resp = self.client.get('/')
        resp_data = resp.get_data(as_text=True)
        self.assertTrue('您好, 陌生人' in resp_data)

    def test_register_login_logout(self):
        """ 测试注册，登录，登出
        """
        # 测试注册
        resp = self.client.post('/auth/register', data={
            'email': 'chenjiandongx@qq.com',
            'username': 'Admin',
            'password': 'default',
            'password_confirm': 'default'
        })
        self.assertTrue(resp.status_code == 302)    # 302 代表重定向

        # 测试登录
        resp = self.client.post('/auth/login', data={
            'email': 'chenjiandongx@qq.com',
            'password': 'default',
        }, follow_redirects=True)
        resp_data = resp.get_data(as_text=True)
        self.assertTrue('您目前还没有确认您的账户' in resp_data)

        # 使用令牌验证用户
        user = User.query.filter_by(email='chenjiandongx@qq.com').first()
        token = user.generate_confirmation_token().decode('utf-8')
        resp = self.client.get('/auth/confirm/' + token, follow_redirects=True)
        resp_data = resp.get_data(as_text=True)
        self.assertTrue('您好, Admin' in resp_data)
        self.assertTrue('您已经确认过您的账户了' in resp_data)

        # 退出登录
        resp = self.client.get('/auth/logout', follow_redirects=True)
        resp_data = resp.get_data(as_text=True)
        self.assertTrue('您好, 陌生人' in resp_data)
        self.assertTrue('您已退出登录' in resp_data)
