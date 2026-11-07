import json
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import model


def load_room():
    # with open ("json/room.json", encoding = "utf-8") as f:
    #     return json.load(f)
    return model.PhongHat.query.all()


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


def check_login(username = None, password = None):
    customers = read_json_account()
    for customer in customers:
        if customer.get('USERNAME') == username and password != None:
            #check password hash là hàm trong thư viện werkzeug 
            if check_password_hash(customer.get('PASSWORD'), password):
                #trả về tên và role để hiển thị lên sau khi đăng nhập
                return [customer['TENKH'], "CLIENT"]

    staff_owner = read_json_account("json/nhanvien_owner.json")
    for staff in staff_owner:
        if staff.get('USERNAME') == username and password != None:
            if check_password_hash(staff.get('PASSWORD'), password):
                return [staff['TENNV'], staff['ROLE']]
    return None



# if __name__== "__main__":
#     print(check_login('staff','staff123')[0])