# 基于 Python Flask 的微博系统

[![Build Status](https://travis-ci.org/chenjiandongx/jianweibo.svg?branch=master)](https://travis-ci.org/chenjiandongx/jianweibo)

![jianweibo](https://github.com/chenjiandongx/jianweibo/blob/master/images/jianweibo.png)

简微博已部署在 heroku，[https://jianweibo.herokuapp.com/](https://jianweibo.herokuapp.com/)，欢迎前往体验

开发环境：Windows10 + Python3

### PC 端

首页

![pc-0](https://github.com/chenjiandongx/jianweibo/blob/master/images/pc-0.gif)

个人信息页

![pc-1](https://github.com/chenjiandongx/jianweibo/blob/master/images/pc-1.gif)

注册

![pc-2](https://github.com/chenjiandongx/jianweibo/blob/master/images/pc-2.png)


### 移动端

首页

![mobile-0](https://github.com/chenjiandongx/jianweibo/blob/master/images/mobile-0.gif)

个人信息页

![mobile-1](https://github.com/chenjiandongx/jianweibo/blob/master/images/mobile-1.gif)

注册

![mobile-2](https://github.com/chenjiandongx/jianweibo/blob/master/images/mobile-2.png)

得益于 [flask-boostrap](https://github.com/mbr/flask-bootstrap)，自适应 PC 端和移动端。不过毕竟免费，部署在 Heroku 速度一般吧。


## 项目介绍

[Flask](https://github.com/pallets/flask) 是基于 Pyhton 的 Web 开发框架，我觉得它的最大特点就是自由，框架本身提供了必备的所有内容，然后更多的功能的实现更依赖于第三方插件。也就是说，当你不满足现有的解决方案的时候你甚至可以给自己的 Web 项目动手写个增强插件来。

了解一个框架最好的方法就是动手实现一个项目，这个项目基本上是参照 [Flask Web Development
Developing Web Applications with Python](http://shop.oreilly.com/product/0636920031116.do) 这本书一行一行码出来的，不过对很多东西进行了修改。作者在 Github 上有这本书源码对应的仓库 [https://github.com/miguelgrinberg/flasky](https://github.com/miguelgrinberg/flasky)。

不过说句实在的，这本书项目还是有些大大小小的 bug，而且有些地方其实是可以优化代码的。当你自己一行一行码出来就会知道了。直接签出源码仓库运行会发现直接就报错的 -_-! 世上无难事，只要有 Google。

## 插件
项目使用的第三方插件

* [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap)
* [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth)
* [Flask-Login](https://github.com/maxcountryman/flask-login)
* [Flask-Mail](https://github.com/mattupstate/flask-mail)
* [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)
* [Flask-RESTful](https://github.com/flask-restful/flask-restful)
* [Flask-Script](https://github.com/smurfix/flask-script)
* [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
* [Flask-SSLify](https://github.com/kennethreitz/flask-sslify)
* [Flask-WTF](https://github.com/lepture/flask-wtf)


## RESTful API

RESTful 部分是使用了 [flask-restful](https://github.com/flask-restful/flask-restful) 插件来完成的。下面是使用 [httpie](https://github.com/jakubroztocil/httpie) 在终端下的测试结果

### 评论
获取全部评论信息：https://jianweibo.herokuapp.com/api/v1.0/comment
```
$ http https://jianweibo.herokuapp.com/api/v1.0/comment
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 325
Content-Type: application/json
Date: Tue, 26 Sep 2017 14:57:59 GMT
Server: gunicorn/19.7.1
Via: 1.1 vegur

{
    "comment": [
        {
            "authorID": 1,
            "post": "Interesting",
            "postID": 203,
            "postTime": "Mon, 25 Sep 2017 14:19:40 GMT"
        },
        {
            "authorID": 1,
            "post": "Interesting",
            "postID": 203,
            "postTime": "Mon, 25 Sep 2017 14:19:31 GMT"
        }
    ],
    "totalCommentsCount": 2
}
```

获取单条评论信息：https://jianweibo.herokuapp.com/api/v1.0/comment/<int:id>
```
$ http https://jianweibo.herokuapp.com/api/v1.0/comment/1
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 112
Content-Type: application/json
Date: Tue, 26 Sep 2017 14:59:37 GMT
Server: gunicorn/19.7.1
Via: 1.1 vegur

{
    "authorID": 1,
    "post": "Interesting",
    "postID": 203,
    "postTime": "Mon, 25 Sep 2017 14:19:31 GMT"
}

```

### 微博
获取全部微博信息：https://jianweibo.herokuapp.com/api/v1.0/post
```
$ http https://jianweibo.herokuapp.com/api/v1.0/post
Connection: keep-alive
Content-Length: 3674
Content-Type: application/json
Date: Tue, 26 Sep 2017 15:00:31 GMT
Server: gunicorn/19.7.1
Via: 1.1 vegur

{
    "post": [
        {
            "authorID": 7,
            "posTime": "Tue, 19 Sep 2017 00:00:00 GMT",
            "post": "Cras in purus eu magna vulputate luctus. Proin interdum mauris non ligula pellentesque ultrices."
        },
        {
            "authorID": 72,
            "posTime": "Sat, 16 Sep 2017 00:00:00 GMT",
            "post": "Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Duis mattis egestas metus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi."
        },
        {
            "authorID": 54,
            "posTime": "Wed, 20 Sep 2017 00:00:00 GMT",
            "post": "Proin at turpis a pede posuere nonummy. Nunc rhoncus dui vel sem. Duis aliquam convallis nunc."
        },
        {
            "authorID": 8,
            "posTime": "Tue, 05 Sep 2017 00:00:00 GMT",
            "post": "Aenean lectus. Praesent lectus. Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
        },
    .....   # 内容太多，省略后面部分
}
```

获取单条微博信息：https://jianweibo.herokuapp.com/api/v1.0/post/<int:id>
```
$ http https://jianweibo.herokuapp.com/api/v1.0/post/2
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 385
Content-Type: application/json
Date: Tue, 26 Sep 2017 15:01:57 GMT
Server: gunicorn/19.7.1
Via: 1.1 vegur

{
    "authorID": 72,
    "posTime": "Sat, 16 Sep 2017 00:00:00 GMT",
    "post": "Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Duis mattis egestas metus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi."
}

```

发布微博：需要登录用户
```
$ http https://jianweibo.herokuapp.com/api/v1.0/post --auth <your-email>:<your-password>  post="xxxxx"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 16
Content-Type: application/json
Date: Tue, 26 Sep 2017 15:34:08 GMT
Server: gunicorn/19.7.1
Via: 1.1 vegur

{
    "status": 200
}
```

### 用户
获取全部用户信息：https://jianweibo.herokuapp.com/api/v1.0/user
```
$ http https://jianweibo.herokuapp.com/api/v1.0/user
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 1025
Content-Type: application/json
Date: Tue, 26 Sep 2017 15:03:57 GMT
Server: gunicorn/19.7.1
Via: 1.1 vegur

[
    {
        "id": 7,
        "username": "helen"
    },
    {
        "id": 8,
        "username": "joyce"
    },
    {
        "id": 3,
        "username": "fred"
    },
    {
        "id": 4,
        "username": "marilyn"
    },
    {
        "id": 9,
        "username": "jean"
    },
    {
        "id": 5,
        "username": "ruth"
    },
    {
        "id": 6,
        "username": "maria"
    },
    .....   # 内容太多，省略后面部分
}
```

获取单个用户信息：https://jianweibo.herokuapp.com/api/v1.0/user/<int:id>
```
$ http https://jianweibo.herokuapp.com/api/v1.0/user/5
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 159
Content-Type: application/json
Date: Tue, 26 Sep 2017 15:05:35 GMT
Server: gunicorn/19.7.1
Via: 1.1 vegur

{
    "lastSeen": "Sun, 24 Sep 2017 16:46:13 GMT",
    "memberSince": "Fri, 22 Sep 2017 00:00:00 GMT",
    "postCount": 0,
    "posts": [],
    "username": "ruth"
}
```

### 令牌
通过密码获取令牌，然后就可采用令牌登录，不用提交密码
```
$ http https://jianweibo.herokuapp.com/api/v1.0/token --auth <your-email>:<your-password>
```


## 运行程序
新建虚拟环境

``` shell
$ virtualenv venv
# Windows
$ cd venv/Scripts
$ activate
# Linux/MacOs
$ ./venv/Scripts/activate
```

**请确保以后所有的操作都在虚拟环境中运行**

``` shell
$ git clone https://github.com/chenjiandongx/jianweibo.git
$ cd jianweibo
$ pip install -r requirements.txt
$ export FLASK_MODE=default    # Windwos 下使用  set FLASK_MODE=default
$ python manage.py runserver
```
打开 http://127.0.0.1:5000/ 就可以看到程序已经在本地跑起来了


## nose 测试
``` shell
$ cd app
$ nosetests --with-coverage --cover-package=tests --verbosity=2

测试获取全部评论信息 ... ok
测试获取全部微博信息 ... ok
测试获取全部用户信息 ... ok
测试获取指定评论信息 ... ok
测试获取指定微博信息 ... ok
测试获取指定用户信息 ... ok
测试实例已经启动 ... ok
测试使用`TESTING-EMPTY`配置 ... ok
测试首页 ... ok
测试注册，登录，登出 ... ok

Name                            Stmts   Miss  Cover
---------------------------------------------------
__init__.py                        31      2    94%
api_v1_0\__init__.py                3      0   100%
api_v1_0\authentication.py         23     11    52%
api_v1_0\errors.py                  5      2    60%
api_v1_0\models.py                 75     14    81%
auth\__init__.py                    3      0   100%
auth\forms.py                      25      2    92%
auth\views.py                      72     23    68%
decorators.py                      14      3    79%
email.py                           14      0   100%
main\__init__.py                    7      0   100%
main\errors.py                     16     11    31%
main\forms.py                      37      5    86%
main\views.py                     200    148    26%
models.py                         181     47    74%
tests\__init__.py                   0      0   100%
tests\test_api.py                  37      0   100%
tests\test_basics.py               17      0   100%
tests\test_client.py               35      0   100%
D:\Python\jianweibo\config.py      37      6    84%
---------------------------------------------------
TOTAL                             832    274    67%
----------------------------------------------------------------------
Ran 10 tests in 7.344s

OK

```
**代码覆盖主要还是关注 tests 部分**
