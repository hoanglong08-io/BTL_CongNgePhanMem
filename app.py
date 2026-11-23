from flask import Flask, render_template, request, session, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import dao

from db import app
from datetime import datetime
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

@app.template_filter('vnd')
def vnd_filter(value):
    #--> output là số thực tiền.0
    if value is None:
        return "0 VNĐ"
    return "{:.1f} VNĐ".format(float(value))


@app.template_filter('status_label')
def status_label_filter(status):
    return status or ''


@app.template_filter('khung_gio')
def khung_gio_filter(b):
    #định dạng chuỗi thời gian 
    start = getattr(b, 'GIOBATDAU', None)
    end = getattr(b, 'GIOKETTHUC', None)
    if not start:
        return ""
    start_str = start.strftime('%H:%M')
    if end:
        return f"{start_str} - {end.strftime('%H:%M %d/%m/%Y')}"
    return start.strftime('%H:%M %d/%m/%Y')

@app.template_filter('so_tien')
def so_tien_filter(val):
    if not val:
        return "0"
    try:
        return f"{float(val):,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return str(val)

@app.template_filter('vnd')
def vnd_filter(val):
    if not val:
        return "0 VNĐ"
    try:
        return f"{float(val):,.0f} VNĐ".replace(",", ".")
    except (ValueError, TypeError):
        return str(val)

@app.template_filter('ten_phong')
def ten_phong_filter(don):
    if not don:
        return ""
    if hasattr(don, 'phong') and don.phong:
        return getattr(don.phong, 'TENPHONG', '')
    return getattr(don, 'TENPHONG', '')

@app.template_filter('ten_dv')
def ten_dv_filter(item):
    if not item:
        return ""
    if hasattr(item, 'dich_vu') and item.dich_vu:
        return getattr(item.dich_vu, 'TENDV', '')
    return getattr(item, 'TENDV', '')

# route
@app.route("/")
def home():
    # rooms = dao.load_room()
    types= dao.get_room_type()
    start = request.args.get('start_hour', '')
    end = request.args.get("end_hour",'')
    room_type=request.args.get('type','')
    guests=request.args.get('guests','')
    
    rooms=dao.search_room(start_hour=start,end_hour=end,room_type=room_type,num_guests=guests)
    return render_template("index.html", rooms=rooms, types=types, start=start, end=end, guests=guests)
   


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    next_page = request.args.get('next') or request.form.get('next') or ''
    er_message = None
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
            er_message = 'Tên đăng nhập hoặc mật khẩu không chính xác!'

    # Render template kèm biến next_page
    return render_template("login.html", next=next_page, er_message=er_message)
    


@app.route("/logout")
@login_required
def logout():
    # session.clear()
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET','POST'])
def register():
    er_message={}
    if request.method == 'GET':
        return render_template('register.html', er_message=er_message)
    if request.method == 'POST':
        r = request.form
        name = r.get('name')
        phone = r.get('phone')
        username= r.get('username')
        password = r.get('password')

        if phone.isdigit() or len(phone) < 10 or len(phone) > 11:
            er_message['phone'] = 'Số điện thoại không hợp lệ (phải gồm 10 - 11 chữ số)'
        if dao.check_username_exist(username):
            er_message['username'] = 'Tên đăng nhập này đã có người sử dụng.'
            print(er_message.get('username'))
        #theem tk moi vao csdl
        if dao.add_user(name=name, phone=phone, username=username, password=password):
            flash('Đăng ký tài khoản thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Đã xảy ra lỗi hệ thống, vui lòng thử lại sau!', 'danger')
    return render_template('register.html',er_message=er_message)


@app.route('/booking/<int:id>', methods=['GET','POST'])
def booking(id):
    room = dao.get_room_by_id(id)
    if request.method == 'POST':
        start = request.form.get("book_start")
        end = request.form.get("book_end") 
        sl = request.form.get("book_guests")
        phone = request.form.get("customer_phone") or None
        name = request.form.get("customer_name") or None
        makh = None
        if current_user.role == 'CLIENT':
            makh=current_user.id #'KH_..'
            makh=int(makh[3:])
        elif current_user.role in ['STAFF', 'OWNER']:
            makh = dao.get_or_create_walkin_customer(name=name, phone=phone)
        if start >= end:
            er_message = "Giờ kết thúc phải lớn hơn giờ bắt đầu!"
            return render_template("booking_form.html", id= id, er_message=er_message, start=start, end=end, soluong=sl, phone=phone, name=name)
        message, is_done = dao.confirm_booking(start=start, end=end, maphong=id, guests=sl, makh=makh)
        print(is_done, makh)
        luot=dao.dem_luot_trong_thang(makh)
        vouchers = dao.dem_voucher(makh=makh)
        # neu dung
        if is_done:
            print (message)
            return redirect('/my_bookings')
        return render_template("booking_form.html", id= id, message=message, start=start, end=end, soluong=sl, phone=phone, name=name)


    if not current_user.is_authenticated:
        return redirect(url_for('login', next=request.full_path))
    return render_template("booking_form.html",id=id, room_succhua=room.SUCCHUA)

@app.route("/my_bookings")
@login_required
def my_bookings():
    makh =current_user.id
    makh = int(makh[3:])
    luot = dao.dem_luot_trong_thang(makh)
    vouchers = dao.dem_voucher(makh=makh)
    bookings = dao.get_user_booking_history(makh=makh)
    
    return render_template("my_booking.html", bookings=bookings, luot=luot, nguong=10, giam=dao.Decimal(5), vouchers=vouchers)

#-uc 2 gọi món
def lay_don(madat):
    #lấy đơn hàng
    don = dao.get_booking(madat)
    message=''
    makh=current_user.id
    makh=int(makh[3:])
    if current_user.role == "CLIENT" and don.MAKH != makh:
        message = "Chỉ xem được đơn hàng của bản thân"
    return don, message

@app.route("/order/<madat>")
@login_required
def order_page(madat):
    don, message = lay_don(madat)
    items = dao.get_items(don)
    tong = dao.tinh_tong_dich_vu(items)
    if current_user.role in ['STAFF', 'OWNER']:
        quay_lai = url_for("reception")
    else:
        quay_lai = url_for("my_bookings")

    if message or not don:
        flash(message, "danger")
        return redirect(quay_lai)
    return render_template("ordered.html", don=don, menu=dao.get_menu_grouped(),
                           items=items, tong=tong, quay_lai=quay_lai)

@app.route("/order/<madat>/add", methods=["POST"])
@login_required
def order_add(madat):
    don, message = lay_don(madat)

    if current_user.role in ['STAFF', 'OWNER']:
        quay_lai = url_for("reception")
    else:
        quay_lai = url_for("my_bookings")
    so_luong =int(request.form.get('soluong'))
    # 1. Kiểm tra tồn tại đơn và quyền truy cập
    if message or not don:
        flash(message, "danger")
        return redirect(quay_lai)
    madv = request.form.get("madv", "").strip()
    # luu dũ liệu
    nv = current_user if current_user.role in ['STAFF', 'OWNER'] else None
    ok, loi = dao.add_service(don.MADATPHONG, madv, so_luong, nv)

    if ok:
        flash("Đã thêm món vào hóa đơn tạm.", "success")
    else:
        flash(loi or "Thông báo số lượng không hợp lệ hoặc hết hàng.", "danger")

    return redirect(url_for("order_page", madat=madat))

@app.route("/invoice/<madat>")
@login_required
def invoice(madat):
    don = lay_don(madat)
    return render_template("checkout.html", don=don, bill=dao.hoa_don_hien_thi(don), items=dao.get_items(don))


#đã chuyển tiếp được page nếu login thành công (đặt phòng khi chưa login --> login --> chuyển tiếp)
# login, register (success)
# nhấn nút confirm thì bị lỗi chuyển về trang "/"" (success)
#tim kiem phong (success)
# trang bao
# trang thuc don 
# # xu ly du lieu dat phong (done)
# xong lich su dat phòng (done)




if __name__ == "__main__":
    app.run(debug=True, port=4300)
    
