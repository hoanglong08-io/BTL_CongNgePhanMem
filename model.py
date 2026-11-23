from db import db, app
from flask_login import UserMixin


class KhachHang(db.Model, UserMixin):
    __tablename__ = 'KHACH_HANG'

    MAKH = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable = False)
    TENKH = db.Column(db.String(100), nullable=False)
    SDT = db.Column(db.String(15), nullable=False, unique=True)
    USERNAME = db.Column(db.String(50), nullable=False, unique=True)
    PASSWORD = db.Column(db.String(255), nullable=True)

    def get_id(self):
        return str(self.MAKH)


class NhanVien(db.Model, UserMixin):
    __tablename__ = 'NHAN_VIEN'

    MANV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TENNV = db.Column(db.String(100), nullable=False)
    USERNAME = db.Column(db.String(50), unique=True)
    PASSWORD = db.Column(db.String(255))
    ROLE = db.Column(db.String(30))

    def get_id(self):
        return str(self.MANV)


class PhongHat(db.Model):
    __tablename__ = 'PHONG_HAT'

    MAPHONG = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TENPHONG = db.Column(db.String(50))
    LOAIPHONG = db.Column(db.String(50))
    SUCCHUA = db.Column(db.Integer, nullable=False)
    GIATHEOGIO = db.Column(db.Numeric(18, 2), nullable=False)
    TRANGTHAI = db.Column(db.String(30))
    


class DatPhong(db.Model):
    __tablename__ = 'DAT_PHONG'

    MADATPHONG = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MAKH = db.Column(db.Integer, db.ForeignKey('KHACH_HANG.MAKH'), nullable=False)
    MAPHONG = db.Column(db.Integer, db.ForeignKey('PHONG_HAT.MAPHONG'), nullable=False)
    GIOBATDAU = db.Column(db.DateTime, nullable=False)
    GIOKETTHUC = db.Column(db.DateTime, nullable=False)
    SOLUONGNGUOI = db.Column(db.Integer, nullable=False)
    TRANGTHAI = db.Column(db.String(30))




class DichVu(db.Model):
    __tablename__ = 'DICH_VU'

    MADV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TENDV = db.Column(db.String(100), nullable=False)
    GIA = db.Column(db.Numeric(18, 2), nullable=False)
    LOAIDV = db.Column(db.String(50))
    TONKHO = db.Column(db.Integer)

class HoaDon(db.Model):
    __tablename__ = 'HOA_DON'

    MAHD = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MADATPHONG = db.Column(db.Integer, db.ForeignKey('DAT_PHONG.MADATPHONG'), nullable=False, unique=True)
    MANV = db.Column(db.Integer, db.ForeignKey('NHAN_VIEN.MANV'), nullable=False)
    TIENGIO = db.Column(db.Numeric(18, 2), default=0)
    TIENDICHVU = db.Column(db.Numeric(18, 2), default=0)
    PHANTRAMGIAMGIA = db.Column(db.Numeric(5, 2), default=0)
    SOTIENGIAM = db.Column(db.Numeric(18, 2), default=0)
    TIENVAT = db.Column(db.Numeric(18, 2), default=0)
    TONGTIEN = db.Column(db.Numeric(18, 2), default=0)
    NGAYLAPHD = db.Column(db.DateTime)


class ThemDichVu(db.Model):
    __tablename__ = 'THEM_DICHVU'

    MAHD = db.Column(db.Integer, db.ForeignKey('HOA_DON.MAHD'), primary_key=True)
    MADV = db.Column(db.Integer, db.ForeignKey('DICH_VU.MADV'), primary_key=True)
    SOLUONG = db.Column(db.Integer, nullable=False)
    GIA = db.Column(db.Numeric(18, 2), nullable=False)


class LichSuSD(db.Model):
    __tablename__ = 'LICH_SU_SD'

    MALICHSU = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MAKH = db.Column(db.Integer, db.ForeignKey('KHACH_HANG.MAKH'), nullable=False)
    MADATPHONG = db.Column(db.Integer, db.ForeignKey('DAT_PHONG.MADATPHONG'), nullable=False)
    NGAYSUDUNG = db.Column(db.DateTime, nullable=False)
    SOTIENGIAM = db.Column(db.Numeric(18, 2), default=0)


if __name__ == '__main__':
    with app.app_context():
        test = DatPhong.query.first()
        print(test)