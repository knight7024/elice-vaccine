import functools

from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import get_db


bp = Blueprint("auth", __name__, url_prefix="/user")


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        
        db = get_db()
        cursor = db.cursor()
        message, messageType = None, None
                
        if username is None:
            message, messageType = '아이디가 유효하지 않습니다.', 'danger'
        elif password is None:
            message, messageType = '비밀번호가 유효하지 않습니다.', 'danger'
        else:
            cursor.execute(
                'SELECT id FROM user WHERE username = %s', (username, )
            )
            user = cursor.fetchone()
            
            if user is not None:
                message, messageType = f'{username} 계정은 이미 등록된 계정입니다.', 'warning'
            
        if message is None:
            # 유저 테이블에 추가
            cursor.execute(
                'INSERT INTO user (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            # 권한 테이블에 추가
            cursor.execute(
                'INSERT INTO permission (username) VALUES (%s)',
                (username, )
            )
            db.commit()
            return redirect(url_for('auth.signin'))
        
        flash(message=message, category=messageType)

    return render_template('signup.html')


@bp.route('/signin', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        
        db = get_db()
        cursor = db.cursor()
        message, messageType = None, None
        
        cursor.execute(
            'SELECT * FROM user WHERE username = %s', (username, )
        )
        user = cursor.fetchone()

        if user is None:
            message, messageType = '등록되지 않은 계정입니다.', 'danger'
        elif not check_password_hash(user['password'], password):
            message, messageType = '비밀번호가 틀렸습니다.', 'danger'

        if message is None:
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('index'))

        flash(message=message, category=messageType)

    return render_template('signin.html')


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    g.username = None if username is None else username


@bp.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index'))