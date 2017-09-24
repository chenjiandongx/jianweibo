from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('heroku')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    # 启动 shell 时导入所需模块
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """ 部署命令
    """
    from flask_migrate import upgrade
    upgrade()


@manager.command
def generate_data():
    """ 生成用户
    """
    user = User.query.filter_by(email='chenjiandongx@qq.com').first()
    user.role = Role.query.filter_by(permissions=0xff).first()
    db.session.add(user)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
