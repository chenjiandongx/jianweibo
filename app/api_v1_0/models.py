from flask import jsonify, g, request
from flask_restful import Resource, Api, reqparse

from ..models import User, Post, Comment
from .. import db
from .errors import Error
from .authentication import auth
from . import api


restful_api = Api(api)


class UserByIdApi(Resource):
    """
    RESTful API:
        通过 id 获取用户
    """
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return Error.page_not_found
        posts = Post.query.filter_by(author_id=id).all()
        return jsonify(user.to_json([post.body for post in posts]))


class UserApi(Resource):
    """
    RESTful API:
        获取所有用户
    """

    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = User.query.paginate(page, error_out=False)
        users = pagination.items
        if users is None:
            return Error.page_not_found
        userslst = [
            {'username': user.username, 'id': user.id} for user in users]
        userslst.append({'totalUsersCount': pagination.total})
        return jsonify(userslst)


class PostByIdApi(Resource):
    """
    RESTful API:
        通过 id 获取微博
    """

    def get(self, id):
        post = Post.query.filter_by(id=id).first()
        if post is None:
            return Error.page_not_found
        return jsonify(post.to_json())


class PostApi(Resource):
    """
    RESTful API:
        获取所有微博以及发布微博
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('post', type=str, required=True,
                                   help='No post provided', location='json')
        super().__init__()

    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = Post.query.paginate(page, error_out=False)
        posts = pagination.items
        if posts is None:
            return Error.page_not_found
        return jsonify(
            {'post': [post.to_json() for post in posts]})

    # 发布微博需登录状态
    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        post = Post(body=args['post'], author=g.current_user)
        db.session.add(post)
        db.session.commit()
        return {'status': 200}


class CommentByIdApi(Resource):
    """
    RESTful API:
        通过 id 获取评论
    """

    def get(self, id):
        comment = Comment.query.filter_by(id=id).first()
        if comment is None:
            return Error.page_not_found
        return jsonify(comment.to_json())


class CommentApi(Resource):
    """
    RESTful API:
        获取所有评论
    """

    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = Comment.query.paginate(page, error_out=False)
        comments = pagination.items
        if comments is None:
            return Error.page_not_found
        return jsonify({
            'comment': [comment.to_json() for comment in comments],
            'totalCommentsCount': pagination.total
        })


class TokenApi(Resource):
    """
    RESTful API:
        生成验证令牌
    """
    @auth.login_required
    def get(self):
        if g.current_user.is_anonymous or g.token_used:
            return False
        return jsonify({
            'token': g.current_user.generate_auth_token(expiration=3600).decode('utf-8'),
            'expiration': 3600
        })


restful_api.add_resource(UserByIdApi, '/user/<int:id>')
restful_api.add_resource(UserApi, '/user')
restful_api.add_resource(PostByIdApi, '/post/<int:id>')
restful_api.add_resource(PostApi, '/post')
restful_api.add_resource(CommentByIdApi, '/comment/<int:id>')
restful_api.add_resource(CommentApi, '/comment')
restful_api.add_resource(TokenApi, '/token')
