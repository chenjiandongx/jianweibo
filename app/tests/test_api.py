import unittest
import json

from app import create_app


class RestfulApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing-full')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_get_all_users(self):
        """ 测试获取全部用户信息
        """
        resp = self.client.get('/api/v1.0/user')
        j = json.loads(resp.get_data(as_text=True))
        self.assertTrue(j[1]['id'] == 2)
        self.assertTrue(j[1]['username'] == 'Admin')

    def test_get_user(self):
        """ 测试获取指定用户信息
        """
        resp = self.client.get('/api/v1.0/user/2')
        j = json.loads(resp.get_data(as_text=True))
        self.assertTrue(j['username'] == 'Admin')

    def test_get_all_posts(self):
        """ 测试获取全部微博信息
        """
        resp = self.client.get('/api/v1.0/post')
        j = json.loads(resp.get_data(as_text=True))
        self.assertTrue(len(j['post']) == 20)

    def test_get_post(self):
        """ 测试获取指定微博信息
        """
        resp = self.client.get('/api/v1.0/post/1')
        j = json.loads(resp.get_data(as_text=True))
        self.assertTrue(j['authorID'] == 92)

    def test_get_all_comments(self):
        """ 测试获取全部评论信息"""
        resp = self.client.get('/api/v1.0/comment')
        j = json.loads(resp.get_data(as_text=True))
        self.assertTrue(j['totalCommentsCount'] == 1)

    def test_get_comment(self):
        """ 测试获取指定评论信息"""
        resp = self.client.get('/api/v1.0/comment/1')
        j = json.loads(resp.get_data(as_text=True))
        self.assertTrue(j['authorID'] == 1)
        self.assertTrue(j['post'] == '777？')
