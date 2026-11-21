import json, hashlib
from flask_login import UserMixin
from model import PhongHat, DatPhong, NhanVien, KhachHang, DichVu, HoaDon, LichSuSD, ThemDichVu

from model import db
from db import type_room_text

def load_room():
    # with open ("json/room.json", encoding = "utf-8") as f:
    #     return json.load(f)
    return PhongHat.query.all()

def get_room_type():
    types_raw=db.session.execute(type_room_text).fetchall()
    types=[row[0] for row in types_raw]
    return types

class User(UserMixin):
    def __init__(self, id, name, username, role, phone=None):
        self.id = str(id)
        self.name = name
        self.username = username
        self.role = role
        self.phone = phone

    def __str__(self):
        return f"<User id='{self.id}', name='{self.name}', role='{self.role}'>"




def search_room(guest=2, type=None, trang_thai="Available"):
    with open("json/room.json", encoding="utf-8") as f:
        rooms = json.load(f) 
        rooms = [r for r in rooms if guest <= r['capacity'] and r['status'].__eq__(trang_thai)]
        if type:
            rooms = [r for r in rooms if r['type'].__eq__(type)]
        return rooms

# def read_json_account(path = "json/khachhang.json"):
#     with open (path, "r", encoding = "utf-8") as f:
#         return json.load(f)


def get_user_by_username(username):
    """Tìm user (KhachHang hoặc NhanVien) theo username."""
    kh = KhachHang.query.filter_by(USERNAME=username).first()
    if kh:
        return kh
    nv = NhanVien.query.filter_by(USERNAME=username).first()
    return nv

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


def check_username_exist(username):
    return KhachHang.query.filter_by(USERNAME=username).first is not None

def verify_password(user, password):
    if not user or not user.PASSWORD:
        return False
    return user.PASSWORD == hashlib.md5(password.encode('utf-8')).hexdigest()

def add_user(name, phone, username, password):
    try:
        # 1. Băm mật khẩu trước khi lưu
        hashed_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()

        # 2. Khởi tạo đối tượng Model với dữ liệu từ form
        new_user = KhachHang(
            TENKH=name,
            SDT=phone,
            USERNAME=username,
            PASSWORD=hashed_pwd
            # Nếu có thêm các trường như role, bạn có thể gán mặc định: role='CLIENT'
        )

        # 3. Đưa vào Session và Commit xuống MySQL
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



if __name__== "__main__":
    from db import app
    with app.app_context():
        # user = get_user_by_id('NV_01')
        # print(user)

        print(get_room_type())
    # psw = "staff456"
    # psw = hashlib.md5(psw.encode('utf-8')).hexdigest()
    # print(psw)
    
    