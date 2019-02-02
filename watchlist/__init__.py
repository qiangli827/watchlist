# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)

# 注册环境变量
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

# 实例化扩展类
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    #载入用户到登录中
    user = User.query.get(int(user_id))
    return user
# 认证保护
login_manager.login_view = 'login'

from watchlist import views, errors, commands
