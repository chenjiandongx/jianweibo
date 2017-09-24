from flask import (render_template, redirect, url_for, current_app,
                   abort, flash, request, make_response)
from flask_login import login_required, current_user

from . import main
from .forms import (PostForm, EditProfileForm, EditProfileAdminForm,
                    CommentForm, SearchUserForm)
from .. import db
from ..decorators import admin_required, permission_required
from ..models import User, Role, Post, Permission, Comment


@main.route('/', methods=['GET', 'POST'])
def index():
    """ 视图首页，发表微博
    """
    form = PostForm()
    if form.validate_on_submit() and current_user.can(Permission.WRITE_ARTICLES):
        _post = Post(body=form.body.data,
                     author=current_user._get_current_object())
        db.session.add(_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    _show_followed = False
    if current_user.is_authenticated:
        _show_followed = bool(request.cookies.get('show_followed', ''))
    if _show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query

    page = request.args.get('page', 1, type=int)        # 默认为第 1 页
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html',
                           form=form,
                           posts=posts,
                           pagination=pagination)


@main.route('/all')
@login_required
def show_all():
    """ 显示所有用户微博
    """
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    """ 仅显示关注着微博
    """
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/user/<username>')
def user(username):
    """ 查看指定用户信息

    :param username: 指定用户
    """
    _user = User.query.filter_by(username=username).first()
    if _user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = _user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html',
                           posts=posts,
                           user=_user,
                           pagination=pagination)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    """ 发表评论

    :param id: 微博 id
    """
    _post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=_post,
                          author=current_user._get_current_object())
        # comment 的 author 字段不能直接设置为 current_user，因为这个变量是上下文代理
        # 对象。真正的 User 对象要使用 current_user._get_current_object() 获取
        db.session.add(comment)
        db.session.commit()
        flash('您已经成功提交评论')
        return redirect(url_for('.post', id=_post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (_post.comments.count() - 1) / \
               current_app.config['FLASK_POSTS_PER_PAGE'] + 1        # 20 为每页评论条数
    pagination = _post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template("post.html",
                           posts=[_post],
                           form=form,
                           pagination=pagination,
                           comments=comments)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """ 更新微博

    :param id: 微博 id
    """
    _post = Post.query.get_or_404(id)
    if current_user != _post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        _post.body = form.body.data
        db.session.add(_post)
        db.session.commit()
        flash("微博已经更新")
        return redirect(url_for('.post', id=_post.id))
    form.body.data = _post.body
    return render_template('edit_post.html', form=form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """ 删除指定微博

    :param id: 微博 id
    """
    _post = Post.query.get_or_404(id)
    if current_user != _post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    db.session.delete(_post)
    db.session.commit()
    flash('您已删除该微博')
    return redirect(url_for('.index'))


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ 用户编辑资料
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username and \
                User.query.filter_by(username=form.username.data).first():
            flash('该用户名已被使用')
            return redirect(url_for('.edit_profile'))
        current_user.username = form.username.data
        current_user.realname = form.realname.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.sex = form.sex.data
        db.session.add(current_user)
        db.session.commit()
        flash('您已经更新了个人资料')
        return redirect(url_for('main.user', username=current_user.username))
    form.username.data = current_user.username
    form.realname.data = current_user.realname
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.sex.data = current_user.sex
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    """ 管理员编辑资料

    :param id: 用户 id
    """
    _user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=_user)
    if form.validate_on_submit():
        _user.username = form.username.data
        _user.realname = form.realname.data
        _user.confirmed = form.confirmed.data
        _user.role = Role.query.get(form.role.data)
        _user.location = form.location.data
        _user.about_me = form.about_me.data
        db.session.add(_user)
        db.session.commit()
        flash('资料已更新')
        return redirect(url_for('main.user', username=_user.username))
    form.username.data = _user.username
    form.confirmed.data = _user.confirmed
    form.role.data = _user.role_id
    form.realname.data = _user.realname
    form.location.data = _user.location
    form.about_me = _user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    """ 关注指定用户

    :param username: 指定用户名
    """
    _user = User.query.filter_by(username=username).first()
    if _user is None:
        flash('该用户不存在')
        return redirect(url_for('main.index'))
    if current_user.is_following(_user):
        flash('您已经关注了该用户')
        return redirect(url_for('main.user', username=username))
    current_user.set_follow(_user)
    flash('您关注了该用户')
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    """ 取消关注指定用户

    :param username: 指定用户名
    """
    _user = User.query.filter_by(username=username).first()
    if user is None:
        flash('该用户不存在')
        return redirect(url_for('main.index'))
    if current_user.is_following(_user):
        current_user.set_unfollow(_user)
        flash('您已取消关注该用户')
        return redirect(url_for('main.user', username=username))
    return redirect(url_for('main.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    """ 查看指定用户关注者名单

    :param username: 指定用户名
    """
    _user = User.query.filter_by(username=username).first()
    if _user is None:
        flash('该用户不存在')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = _user.followers.paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html',
                           user=_user,
                           title="粉丝",
                           pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    """ 查看指定用户被关注者名单

    :param username: 指定用户名
    """
    _user = User.query.filter_by(username=username).first()
    if _user is None:
        flash('该用户不存在')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = _user.followed.paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html',
                           user=_user,
                           title="关注",
                           pagination=pagination,
                           follows=follows)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    """ 评论管理
    """
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html',
                           comments=comments,
                           pagination=pagination,
                           page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    """ 恢复已屏蔽评论

    :param id: 评论 id
    """
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('main.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    """ 屏蔽评论

    :param id: 评论 id
    """
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('main.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/search-user', methods=['GET', 'POST'])
def search_user():
    """ 搜索用户
    """
    form = SearchUserForm()
    if form.validate_on_submit():
        _user = User.query.filter_by(username=form.username.data).first()
        if _user is None:
            flash('该用户不存在')
            return redirect(url_for('main.search_user'))
        return redirect(url_for('main.user', username=form.username.data))
    return render_template('search_user.html', form=form)
