from flask import Flask, render_template, request, session, redirect, flash, url_for
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


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    # Lấy tham số next từ cả Query String (GET) lẫn Form ngầm (POST)
    next_page = request.args.get('next') or request.form.get('next') or ''

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username, password)
        if user:
            login_user(user=user)
            # Nếu có trang đang chờ (next_page) thì chuyển hướng tới đó
            if next_page:
                return redirect(next_page)
            return redirect('/')
        else:
            flash('Tên đăng nhập hoặc mật khẩu không chính xác!', 'danger')

    # Khi vào bằng GET hoặc Đăng nhập thất bại -> Render template kèm biến next_page
    return render_template("login.html", next=next_page)
    

    # if current_user.is_authenticated:
    #     return redirect('/')

    # next_page = request.args.get('next', '')
    # error = None

    # if request.method == 'POST':
    #     username = request.form.get('username', '').strip()
    #     password = request.form.get('password', '').strip()
    #     next_page = request.form.get('next', '')

    #     user = dao.get_user_by_username(username)
    #     if user and dao.verify_password(user, password):
    #         login_user(user)
    #         flash(f'Chào mừng {user.ten}!', 'success')
    #         if next_page and next_page.startswith('/'):
    #             return redirect(next_page)
    #         return redirect('/')
    #     else:
    #         error = 'Sai tên đăng nhập hoặc mật khẩu. Vui lòng nhập lại.'

    # return render_template('login.html', next=next_page, error=error)


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


@app.route('/booking/<int:id>', methods=['GET','POST'])
def booking(id):

    if request.method == 'POST':
        start = request.form.get("book_start")
        end = request.form.get("book_end")
        sl = request.form.get("sl")
        phone = request.form.get("phone") or None
        name = request.form.get("name") or None
        #xử lý csdl ở đây
        
        return redirect("/")

    if not current_user.is_authenticated:
        return redirect(url_for('login', next=request.full_path))
    
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    sl = request.args.get("sl", "2")

    if current_user.role == 'CLIENT':
        phone = getattr(current_user, 'phone', '')
        name = getattr(current_user, 'name', '')
    else:
        phone = request.args.get("phone", "")
        name = request.args.get("name", "")
    return render_template("booking_form.html",id=id,start=start,end=end,sl=sl,phone=phone,name=name)

#đã chuyển tiếp được page nếu login thành công (đặt phòng khi chưa login --> login --> chuyển tiếp)

# nhấn nút confirm thì bị lỗi chuyển về trang "/""
# trên url chưa hiển thị thông tin như mong muốn: 
# /booking/id phong/start=giờ bắt đầu&end=giờ kết thúc&sl=số lượng&phone=điện thoại khách hàng&name=tên khách hàng
# nếu đặt từ client thì phone và name gán từ tài khoản đó
# nếu đặt từ nhân viên thì phone và name gán từ form khi submit lên

if __name__ == "__main__":
    app.run(debug=True, port=4300)