import json, hashlib, math
from flask_login import UserMixin
from model import PhongHat, DatPhong, NhanVien, KhachHang, DichVu, HoaDon, LichSuSD, ThemDichVu
from datetime import datetime, date, timedelta
from decimal import Decimal


from model import db
from db import type_room_text

datetime_f="%Y-%m-%d %H:%M"
current_day = date.today() 

def load_room():
    # with open ("json/room.json", encoding = "utf-8") as f:
    #     return json.load(f)
    return PhongHat.query.filter_by(TRANGTHAI='Available')

def get_room_type():
    types_raw=db.session.execute(type_room_text).fetchall()
    types=[row[0] for row in types_raw]
    return types
def get_room_by_id(id):
    return PhongHat.query.get(id)

class User(UserMixin):
    def __init__(self, id, name, username, role, phone=None):
        self.id = str(id)
        self.name = name
        self.username = username
        self.role = role
        self.phone = phone

    def __str__(self):
        return f"<User id='{self.id}', name='{self.name}', role='{self.role}'>"

#ép kieu time
def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None
    
def parse_datetime(time_str):
    full_datetime=f"{current_day} {time_str}"
    try:
        return datetime.strptime(full_datetime, datetime_f)
    except ValueError:
        return None


def search_room(start_hour, end_hour, room_type, num_guests):
    query = PhongHat.query.filter(PhongHat.TRANGTHAI != 'Maintenance')
    start_t = parse_time(start_hour)
    end_t = parse_time(end_hour)

    #lọc giờ
    if start_t and end_t:
        booked_room_ids = db.session.query(DatPhong.MAPHONG).filter(
            db.func.time(DatPhong.GIOBATDAU) < end_t,
            db.func.time(DatPhong.GIOKETTHUC) > start_t,
            DatPhong.TRANGTHAI != 'Cancelled'
        ).subquery()

        query = query.filter(~PhongHat.MAPHONG.in_(booked_room_ids))

    #lọc loại phòng
    if room_type and str(room_type).strip():
        query = query.filter(PhongHat.LOAIPHONG == str(room_type).strip())

    #lọc so luong khách
    if num_guests and str(num_guests).isdigit():
        query = query.filter(PhongHat.SUCCHUA >= int(num_guests))

    return query.all()


def confirm_booking(start, end, maphong, guests, makh):
    start = parse_datetime(start)
    end = parse_datetime(end)
    try:
        
        dp = DatPhong(MAKH=makh, MAPHONG=maphong, GIOBATDAU=start, GIOKETTHUC=end, SOLUONGNGUOI=guests, TRANGTHAI="Booked")
        db.session.add(dp)
        room = PhongHat.query.get(maphong)
        room.TRANGTHAI = 'Occupied'
        db.session.commit()
        return "Đặt phòng thành công", True
    except Exception as e:
        print({e})
        db.session.rollback()
        return "Đặt không thành công, vui lòng thử lại", False

def get_user_booking_history(makh):
    """Lấy danh sách lịch sử đặt phòng của khách hàng kèm tổng tiền hóa đơn (nếu có)."""
    return (db.session.query( DatPhong.MADATPHONG, PhongHat.TENPHONG, DatPhong.GIOBATDAU, DatPhong.GIOKETTHUC, 
                             DatPhong.SOLUONGNGUOI, DatPhong.TRANGTHAI, HoaDon.TONGTIEN)
            .join(PhongHat, DatPhong.MAPHONG == PhongHat.MAPHONG)
            .outerjoin(HoaDon, DatPhong.MADATPHONG == HoaDon.MADATPHONG)
            .filter(DatPhong.MAKH == makh)
            .order_by(DatPhong.GIOBATDAU.desc())
            .all())

def tinh_tien_phong(start, end, price):
    start=parse_datetime(start)
    end=parse_datetime(end)
    total_second = (end-start).total_seconds()
    hours=total_second//3600
    remainin=total_second%3600
    #loos 10 phut se thanh 1 tieng
    if remainin >= 600:
        hours+=1
    total_price = hours * price
    return hours, total_price

# def read_json_account(path = "json/khachhang.json"):
#     with open (path, "r", encoding = "utf-8") as f:
#         return json.load(f)


def get_customer_by_username(username):
    try:
        kh = KhachHang.query.filter_by(USERNAME=username).first()
        return kh
    except Exception as e:
        print({e})
        return None

def get_user_by_id(user_id):
    str_id=str(user_id )
    id = int(str_id[3:])
    if str_id.startswith('KH_'):
        kh=KhachHang.query.filter_by(MAKH=id).first()
        if kh:
            return User(id=f'KH_{kh.MAKH}', name=kh.TENKH, username=kh.USERNAME, role='CLIENT', phone=kh.SDT)
    if str_id.startswith('NV_'):
        nv=NhanVien.query.filter_by(MANV=id).first()
        if nv:
            return User(id=f'NV_{nv.MANV}', name=nv.TENNV, username=nv.USERNAME, role=nv.ROLE)
    
    return None


def get_or_create_walkin_customer(name, phone):
    username_temp = f"{name}:{phone}"
    existing_kh = KhachHang.query.filter(
        (KhachHang.SDT == phone) | (KhachHang.USERNAME == username_temp)
    ).first()
    if existing_kh:
        return existing_kh.MAKH  # MAKH đã tồn tại
    # chua tung ghe truoc day (vang lai)
    try:
        new_kh = KhachHang( TENKH=name, SDT=phone, USERNAME=username_temp, PASSWORD=None)
        db.session.add(new_kh)
        db.session.commit()
        return new_kh.MAKH  # MAKH mới vừa tự động sinh 
    except Exception as e:
        print(f"Lỗi tạo khách vãng lai: {e}")
        db.session.rollback()
        return None

def check_username_exist(username):
    return KhachHang.query.filter_by(USERNAME=username).first is not None

def verify_password(user, password):
    if not user or not user.PASSWORD:
        return False
    return user.PASSWORD == hashlib.md5(password.encode('utf-8')).hexdigest()

def add_user(name, phone, username, password=None):
    try:
        # Băm mật khẩu trước khi lưu
        if password:
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
        new_user = KhachHang( TENKH=name, SDT=phone, USERNAME=username, PASSWORD=password)
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi khi lưu CSDL: {e}")
        db.session.rollback()  # Hoàn tác nếu gặp lỗi
        return False


def check_login(username = None, password = None):
    # customers = read_json_account()
    customer = KhachHang.query.filter_by(USERNAME=username).first()

    # print(customer.PASSWORD, end='\n')
    # print(hashlib.md5(password.encode('utf-8')).hexdigest())

    if customer and customer.PASSWORD:
        if verify_password(customer, password):
            return User(id=f"KH_{customer.MAKH}", name=customer.TENKH, username=customer.USERNAME, role="CLIENT", phone=customer.SDT)
    # staff_owner = read_json_account("json/nhanvien_owner.json")
    staff = NhanVien.query.filter_by(USERNAME=username).first()
    if staff and staff.PASSWORD:
        if verify_password(staff,password):
            # Dùng staff.MANV, staff.TENNV, staff.ROLE (dấu chấm, không dùng ['...'])
            return User(id=f"NV_{staff.MANV}", name=staff.TENNV, username=staff.USERNAME, role=staff.ROLE)
        
    return None


def dau_thang(moc):
    return moc.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def dau_thang_sau(moc):
    return (dau_thang(moc) + timedelta(days=32)).replace(day=1)

def dem_luot_trong_thang(makh, moc=None):
    moc = moc or datetime.now()
    so_luot = (db.session.query(db.func.count(HoaDon.MAHD)).select_from(HoaDon)
               .join(DatPhong, DatPhong.MADATPHONG == HoaDon.MADATPHONG)
               .filter(DatPhong.MAKH == makh, DatPhong.TRANGTHAI == "Completed",
                       HoaDon.NGAYLAPHD >= dau_thang(moc),
                       HoaDon.NGAYLAPHD < dau_thang_sau(moc))
               .scalar())
    return so_luot or 0

def dem_voucher(makh):
    return LichSuSD.query.filter(LichSuSD.MAKH == makh, LichSuSD.SOTIENGIAM > 0).count()

if __name__== "__main__":
    from db import app
    with app.app_context():
    #     # user = get_user_by_id('NV_01')
    #     # print(user)

    #     print(get_room_type())
    # psw = "staff456"
    # psw = hashlib.md5(psw.encode('utf-8')).hexdigest()
    # print(psw)
    # print(parse_datetime("14:30"), type(parse_datetime("14:30")))
    # start, end = confirm_booking("14:30", "15:00")
    # print(start, type(start), end='\n')
    # print(end, type(end), end='\n')
    
        gio, phi=tinh_tien_phong("14:30", "15:32", 100000)
        print(gio, phi)

        print(dem_voucher(1))