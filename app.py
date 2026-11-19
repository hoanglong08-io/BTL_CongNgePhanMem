from flask import Flask, render_template, request, session, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
import dao

from db import app

from flask_login import LoginManager, login_user, logout_user, login_url, login_required, current_user
from flask_admin import BaseView, expose


# app = Flask(__name__)
app.secret_key = 'karaoke_secret_key'

#flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Tên hàm route trang đăng nhập
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này!'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/")
def home():
    rooms = dao.load_room()
    types = dao.load_room()
    return render_template("index.html", rooms=rooms)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username, password)
        if user:
            # lưu lại phiên làm việc
            # session['username'] = username
            # session['name'] = user[0]
            # session['role'] = user[1]
            # print(session)
            login_user(user=user)
            return redirect('/')
        
        else:
            flash ('Tên đăng nhập hoặc mật khẩu không chính xác!')
            return redirect('/login')
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    # session.clear()
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        r = request.form
        user = r.get('name')
        phone = r.get('phone')
        password = r.get('password')
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True, port=4300)