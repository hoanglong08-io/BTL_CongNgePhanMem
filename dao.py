import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from model import PhongHat, DatPhong, NhanVien, KhachHang, DichVu, HoaDon, LichSuSD, ThemDichVu


def load_room():
    # with open ("json/room.json", encoding = "utf-8") as f:
    #     return json.load(f)
    return PhongHat.query.all()


class User(UserMixin):
    def __init__(self, id, name, username, role):
        self.id = str(id)
        self.name = name
        self.username = username
        self.role = role

    def __str__(self):
        return f"<User id='{self.id}', name='{self.name}', role='{self.role}'>"


def search_room(guest=2, type=None, trang_thai="Available"):
    with open("json/room.json", encoding="utf-8") as f:
        rooms = json.load(f) 
        rooms = [r for r in rooms if guest <= r['capacity'] and r['status'].__eq__(trang_thai)]
        if type:
            rooms = [r for r in rooms if r['type'].__eq__(type)]
        return rooms

def read_json_account(path = "json/khachhang.json"):
    with open (path, "r", encoding = "utf-8") as f:
        return json.load(f)


def get_user_by_id(user_id):
    str_id=str(user_id )
    id = int(str_id[3:])
    if str_id.startswith('KH_'):
        kh=KhachHang.query.filter_by(MAKH=id).first()
        if kh:
            return User(id=f'KH_{kh.MAKH}', name=kh.TENKH, username=kh.USERNAME, role='CLIENT')

    if str_id.startswith('NV_'):
        nv=NhanVien.query.filter_by(MANV=id).first()
        if nv:
            return User(id=f'NV_{nv.MANV}', name=nv.TENNV, username=nv.USERNAME, role=nv.ROLE)
    
    return None


def check_login(username = None, password = None):
    # customers = read_json_account()
    customer = KhachHang.query.filter_by(USERNAME=username).first()
    if customer and customer.PASSWORD:
        if check_password_hash(customer.PASSWORD, password) or customer.PASSWORD == password:
            return User(id=f"KH_{customer.MAKH}", name=customer.TENKH, username=customer.USERNAME, role="CLIENT")

    # staff_owner = read_json_account("json/nhanvien_owner.json")

    staff = NhanVien.query.filter_by(USERNAME=username).first()
    if staff and staff.PASSWORD:
        if check_password_hash(staff.PASSWORD, password) or staff.PASSWORD == password:
            # Dùng staff.MANV, staff.TENNV, staff.ROLE (dấu chấm, không dùng ['...'])
            return User(id=f"NV_{staff.MANV}", name=staff.TENNV, username=staff.USERNAME, role=staff.ROLE)
        
    return None



# if __name__== "__main__":
#     from db import app
#     with app.app_context():
#         user = get_user_by_id('NV_01')
#         print(user)