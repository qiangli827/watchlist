# -*- coding: utf-8 -*-
from watchlist import app, db
from watchlist.models import User, Movie
from flask import url_for, render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user



@app.route('/', methods=['GET', 'POST'])
def index():
    # 这部分是添加表单
    if request.method == 'POST':
        # 认证保护
        if not current_user.is_authenticated:
            flash('you need to login to add items')
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash('invalid input')
            return redirect(url_for('page_404'))
        # 保存数据
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('item created')
        return redirect(url_for('index'))
    #这部分是显示电影清单
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    # 如果要编辑
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year)>4 or len(title)>60:
            flash('invalid input')
            # 如果未通过数据验证,返回原先编辑页面
            return redirect(url_for('edit', movie_id=movie_id))
        # 如果通过验证,则更新数据
        movie.title = title
        movie.year = year
        db.session.commit()
        # 提示成功,返回主页
        flash('item updated')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie) #传入编辑的电影

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('item deleted')
    return redirect(url_for('index'))

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='qiangli'))
    return url_for('test_url_for', name='qiangli')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('invalid input')
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证用户密码
        if username==user.username and user.validate_password(password):
            login_user(user)
            flash('login succeed')
            return redirect(url_for('index'))
        flash('invalid username or password')
        return redirect('login')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('goodbye')
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('invalid input')
            return redirect(url_for('settings'))
        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('settings updated')
        return redirect(url_for('index'))
    return render_template('settings.html')
