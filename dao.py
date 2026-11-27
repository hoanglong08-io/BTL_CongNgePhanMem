import json, hashlib, math
from flask_login import UserMixin
from model import PhongHat, DatPhong, NhanVien, KhachHang, DichVu, HoaDon, LichSuSD, ThemDichVu
from datetime import datetime, date, timedelta
from decimal import Decimal


from model import db
from query import (type_room_text, booking_history_cus,get_all_services_text,get_booking_by_id_text,get_ordered_items_text,get_hoadon_by_booking_text
                   ,get_them_dichvu_item_text, get_status_room_text, get_booking_reception_text, auto_update_booking_status_text, auto_update_room_status_text)

datetime_f="%Y-%m-%d %H:%M"

current_day = date.today() 
current_datetime = datetime.now()

class User(UserMixin):
    def __init__(self, id, name, username, role, phone=None):
        self.id = str(id)
        self.name = name
        self.username = username
        self.role = role
        self.phone = phone

    def __str__(self):
        return f"<User id='{self.id}', name='{self.name}', role='{self.role}'>"

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

def get_customer_by_username(username):
    try:
        kh = KhachHang.query.filter_by(USERNAME=username).first()
        return kh
    except Exception as e:
        print({e})
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

def get_status_room_func():
    row = db.session.execute(get_status_room_text).fetchall()
    trang_thai_phong = [r[0] for r in row]
    return trang_thai_phong
def get_rooms():
    return PhongHat.query.all()

def get_booking_receptions():
    return db.session.execute(get_booking_reception_text).fetchall()

#ép kieu time
def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None

def parse_datetime(dt):
    return datetime.strftime(dt, datetime_f)

def date_time_concate(time_str):
    full_datetime=f"{current_day} {time_str}"
    print(full_datetime)
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

def get_duration_hour(start, end):
    if type(start) == str:
        start=date_time_concate(start)
    if type(end) == str:
        end=date_time_concate(end)
    total_second = (end-start).total_seconds()
    hours=total_second//3600
    remainin=total_second%3600
    #loos 10 phut se thanh 1 tieng
    if remainin >= 600:
            hours+=1
    return hours


def tinh_tien_phong(start, end, price):
    hours = get_duration_hour(start=start, end=end)
    hours_dec = Decimal(str(hours))
    price_dec = Decimal(str(price))

    total_price = hours_dec * price_dec
    return hours, total_price

def confirm_booking(start, end, maphong, guests, makh):
    print(start)
    start = date_time_concate(start)
    
    end = date_time_concate(end)
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



def auto_start_booking_status():
    #tự động cập nhật khi tới giờ
    try:
        now = datetime.now()
        # Chạy SQL cập nhật đơn Booked -> InUse
        db.session.execute(auto_update_booking_status_text, {"now": now})
        # Chạy SQL cập nhật phòng Available -> Occupied
        db.session.execute(auto_update_room_status_text)
        # Commit để lưu thay đổi xuống CSDL
        db.session.commit()
    except Exception as e:
        print(f"Lỗi tự động cập nhật trạng thái: {e}")
        db.session.rollback()

def get_booking_receptions():
    # tự động cập nhật trạng thái
    auto_start_booking_status()
    return db.session.execute(get_booking_reception_text).fetchall()

def cancel_booking(madat):
    # hủy đặt
    try:
        dp = DatPhong.query.get(madat)
        if not dp:
            return False, "Đơn đặt phòng không tồn tại."
        
        dp.TRANGTHAI = "Cancelled"
        phong = PhongHat.query.get(dp.MAPHONG)
        if phong and phong.TRANGTHAI == "Occupied":
            phong.TRANGTHAI = "Available"
            
        db.session.commit()
        return True, "Hủy đơn thành công."
    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi hủy đơn: {e}"


# lich sử đặt phòng
def get_user_booking_history(makh):
    auto_start_booking_status()
    return db.session.execute(booking_history_cus, {"makh": makh}).all()



# def read_json_account(path = "json/khachhang.json"):
#     with open (path, "r", encoding = "utf-8") as f:
#         return json.load(f)

#đặt cho khách vãng lai
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

#-- uc 2 đặt món
# goji mons
def get_booking_by_id(madat):
    #trả về thông tin của DAT_PHONG dp.MADATPHONG, dp.MAKH, dp.MAPHONG, dp.GIOBATDAU, dp.GIOKETTHUC, dp.SOLUONGNGUOI, dp.TRANGTHAI, ph.TENPHONG, ph.GIATHEOGIO
    return db.session.execute(get_booking_by_id_text, {"madat": madat}).fetchone()

def get_menu_grouped():
    rows = DichVu.query.all()
    grouped = {}
    for r in rows:
        loai = r.LOAIDV or "Khác"
        if loai not in grouped:
            grouped[loai] = []
        grouped[loai].append(r)
    return grouped

def get_mon_da_goi(don):
   # don mang kiểu số hoặc chuỗi
    if type(don) == int or type(don) == str:
        madat = int(don)
    else:
        madat = don.MADATPHONG
    return db.session.execute(get_ordered_items_text, {"madat": madat}).fetchall()

def add_service(madatphong, madv, so_luong, nv=None):
    #thêm dịch vụ (uc2)
    try:
        #hóa đơn tạm
        hd = db.session.execute(get_hoadon_by_booking_text, {"madat": madatphong}).fetchone()
        #chưa thì khởi tạo mới
        if not hd:
            manv = None
            if nv and hasattr(nv, 'id'):
                manv_str = str(nv.id)
                if manv_str.startswith('NV_'):
                    manv = int(manv_str[3:])        
            new_hd = HoaDon(MADATPHONG=madatphong, MANV=manv, TIENDICHVU=0, TONGTIEN=0)
            db.session.add(new_hd)
            db.session.commit()
            mahd = new_hd.MAHD
        else:
            mahd = hd.MAHD
        #lấy đơn giá dịch vụ 
        dv = DichVu.query.get(madv)
        if not dv:
            return False, "Dịch vụ không tồn tại."
        gia = dv.GIA
        # kiểm dịch vụ được chọn
        item = db.session.execute(get_them_dichvu_item_text, {"mahd": mahd, "madv": madv}).fetchone()
        if item:
            # có thì cộng dồn
            tdv_obj = ThemDichVu.query.get((mahd, madv))
            if tdv_obj:
                tdv_obj.SOLUONG += so_luong
        else:
            #chưa thì tạo mới
            new_item = ThemDichVu(MAHD=mahd, MADV=madv, SOLUONG=so_luong, GIA=gia)
            # thêm vào dâtbase
            db.session.add(new_item)

        db.session.commit()
        #tính tiền tôngg
        items = get_mon_da_goi(madatphong)
        tong_dv = tinh_tong_dich_vu(items)
        hd_obj = HoaDon.query.get(mahd)
        if hd_obj:
            hd_obj.TIENDICHVU = tong_dv
            db.session.commit()
        return True, "Đã thêm món vào hóa đơn tạm."

    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi hệ thống: {e}"
# tinh tam 
def get_bill(madp):
    return HoaDon.query.filter_by(MADATPHONG=madp).first()
def tinh_tong_dich_vu(items):
    #tính phí dịch vụ
    tong = 0
    if items:
        for it in items:
            tong += it.SOLUONG * it.GIA
    return tong
def tinh_tong_dich_vu_cua_don(don):
    hd = get_mon_da_goi(don.MADATPHONG)
    if hd:
        return tinh_tong_dich_vu(hd)
    return Decimal(0)
#--uc 3
# hóa đơn
def tinh_tien_hoa_don_tong(don):
    gio, tien_phong=tinh_tien_phong(don.GIOBATDAU,don.GIOKETTHUC, don.GIATHEOGIO)
    tien_dv=tinh_tong_dich_vu_cua_don(don)
    tien_temp=tien_phong + tien_dv
    luot = dem_luot_trong_thang(don.MAKH, current_datetime)
    if luot >= 10:
        giam_pct = Decimal(0.05)
    else:
        giam_pct = Decimal(0)
    giam_tien = tien_temp * giam_pct
    sau_giam = tien_temp - giam_tien
    vat = sau_giam * Decimal(0.10)
    return {"gio": gio, "don_gia": don.GIATHEOGIO, "tien_gio": tien_phong, "tien_dv": tien_dv, "luot": luot, "giam_pct": giam_pct, "giam_tien": giam_tien, 
            "vat": vat, "tong": sau_giam + vat, "da_thanh_toan": False, "ngay_lap": None, "nhan_vien": None}

def thanh_toan_hoa_don(madat, phuong_thuc, user):
    try:
        don = get_booking_by_id(madat)
        if don.TRANGTHAI in ["Completed", "Complete"]:
            return False, "Đơn phòng này đã được thanh toán trước đó."
        manv = None
        if user and hasattr(user, 'role') and user.role in ['STAFF', 'OWNER']:
            user_id_str = str(user.id)
            if user_id_str.startswith('NV_'):
                manv = int(user_id_str[3:])
        
        bay_gio = datetime.now()
        ct = tinh_tien_hoa_don_tong(don)
        don_obj = DatPhong.query.get(madat)
        hd = HoaDon.query.filter_by(MADATPHONG=madat).first()
        if not hd:
            hd = HoaDon(MADATPHONG=madat, MANV=manv, TIENGIO=ct["tien_gio"], TIENDICHVU=ct["tien_dv"], 
                        PHANTRAMGIAMGIA=ct["giam_pct"], SOTIENGIAM=ct["giam_tien"], TIENVAT=ct["vat"], TONGTIEN=ct["tong"], NGAYLAPHD=bay_gio)
            db.session.add(hd)
        else:
            hd.MANV = manv
            hd.TIENGIO = ct["tien_gio"]
            hd.TIENDICHVU = ct["tien_dv"]
            hd.PHANTRAMGIAMGIA = ct["giam_pct"]
            hd.SOTIENGIAM = ct["giam_tien"]
            hd.TIENVAT = ct["vat"]
            hd.TONGTIEN = ct["tong"]
            hd.NGAYLAPHD = bay_gio
        don_obj.TRANGTHAI = "Completed"
        phong = PhongHat.query.get(don.MAPHONG)
        if phong:
            phong.TRANGTHAI = "Available"
        ls = LichSuSD(
            MAKH=don.MAKH,
            MADATPHONG=don.MADATPHONG,
            NGAYSUDUNG=bay_gio,
            SOTIENGIAM=ct["giam_tien"]
        )
        db.session.add(ls)

        db.session.commit()
        print(manv if manv else 0)
        return True, "Thanh toán thành công."

    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi thanh toán: {e}"

def hoa_don_hien_thi(don):
    # tìm hóa đơn
    hd = get_bill(don.MADATPHONG)
    gio, tien_phong=tinh_tien_phong(don.GIOBATDAU,don.GIOKETTHUC, don.GIATHEOGIO)
    # Bước 2: Nếu đơn đã thanh toán xong (Completed) và đã có hóa đơn
    if don.TRANGTHAI == "Completed":
        if hd is not None:
            if hd.NGAYLAPHD is not None:
                # Lấy số liệu cũ đã lưu trong CSDL ra hiển thị
                ket_qua = {
                    "gio": gio,
                    "don_gia": don.GIATHEOGIO,
                    "tien_gio": tien_phong,
                    "tien_dv": hd.TIENDICHVU or 0,
                    "luot": None,
                    "giam_pct": hd.PHANTRAMGIAMGIA or 0,
                    "giam_tien": hd.SOTIENGIAM or 0,
                    "vat": hd.TIENVAT or 0,
                    "tong": hd.TONGTIEN or 0,
                    "da_thanh_toan": True,
                    "ngay_lap": hd.NGAYLAPHD,
                    "nhan_vien": hd.MANV
                }
                return ket_qua

    # Bước 3: Nếu đơn chưa thanh toán thì tính toán hóa đơn tạm tính mới
    return tinh_tien_hoa_don_tong(don)

if __name__== "__main__":
    # from db import app
    # with app.app_context():
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
    
        # gio, phi=tinh_tien_phong("14:30", "15:32", 100000)
        # print(gio, phi)
    print(parse_datetime(current_datetime))
