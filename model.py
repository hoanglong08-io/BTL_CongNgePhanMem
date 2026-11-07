from db import db, app

class KhachHang(db.Model):
    __tablename__ = 'khach_hang'

    MAKH = db.Column(db.String(10), primary_key=True)
    TENKH = db.Column(db.String(100), nullable=False)
    SDT = db.Column(db.String(15), nullable=False, unique=True)
    USERNAME = db.Column(db.String(50), nullable=False, unique=True)
    PASSWORD = db.Column(db.String(255))

    # def __str__(self):
        # return f"<KhachHang MAKH='{self.MAKH}', TENKH='{self.TENKH}', SDT='{self.SDT}', USERNAME='{self.USERNAME}', PASSWORD='{self.PASSWORD}'>"


class NhanVien(db.Model):
    __tablename__ = 'nhan_vien'

    MANV = db.Column(db.String(10), primary_key=True)
    TENNV = db.Column(db.String(100), nullable=False)
    USERNAME = db.Column(db.String(50), unique=True)
    PASSWORD = db.Column(db.String(255))
    ROLE = db.Column(db.String(30))

    # def __str__(self):
        # return f"<NhanVien MANV='{self.MANV}', TENNV='{self.TENNV}', USERNAME='{self.USERNAME}', PASSWORD='{self.PASSWORD}', ROLE='{self.ROLE}'>"


class PhongHat(db.Model):
    __tablename__ = 'phong_hat'

    MAPHONG = db.Column(db.String(10), primary_key=True)
    TENPHONG = db.Column(db.String(50))
    LOAIPHONG = db.Column(db.String(50))
    SUCCHUA = db.Column(db.Integer, nullable=False)
    GIATHEOGIO = db.Column(db.Numeric(18, 2), nullable=False)
    TRANGTHAI = db.Column(db.String(30))

    # def __str__(self):
        # return f"<PhongHat MAPHONG='{self.MAPHONG}', TENPHONG='{self.TENPHONG}', LOAIPHONG='{self.LOAIPHONG}', SUCCHUA={self.SUCCHUA}, GIATHEOGIO={self.GIATHEOGIO}, TRANGTHAI='{self.TRANGTHAI}'>"


class DatPhong(db.Model):
    __tablename__ = 'dat_phong'

    MADATPHONG = db.Column(db.String(10), primary_key=True)
    MAKH = db.Column(db.String(10), db.ForeignKey('khach_hang.MAKH'), nullable=False)
    MAPHONG = db.Column(db.String(10), db.ForeignKey('phong_hat.MAPHONG'), nullable=False)
    GIOBATDAU = db.Column(db.DateTime, nullable=False)
    GIOKETTHUC = db.Column(db.DateTime, nullable=False)
    SOLUONGNGUOI = db.Column(db.Integer, nullable=False)
    TRANGTHAI = db.Column(db.String(30))

    # def __str__(self):
        # return f"<DatPhong MADATPHONG='{self.MADATPHONG}', MAKH='{self.MAKH}', MAPHONG='{self.MAPHONG}', GIOBATDAU='{self.GIOBATDAU}',GIOKETTHUC='{self.GIOKETTHUC}', SOLUONGNGUOI={self.SOLUONGNGUOI}, TRANGTHAI='{self.TRANGTHAI}'>"


class DichVu(db.Model):
    __tablename__ = 'dich_vu'

    MADV = db.Column(db.String(10), primary_key=True)
    TENDV = db.Column(db.String(100), nullable=False)
    GIA = db.Column(db.Numeric(18, 2), nullable=False)
    LOAIDV = db.Column(db.String(50))

    # def __str__(self):
    #     return f"<DichVu MADV='{self.MADV}', TENDV='{self.TENDV}', GIA={self.GIA}, LOAIDV='{self.LOAIDV}'>"


class HoaDon(db.Model):
    __tablename__ = 'hoa_don'

    MAHD = db.Column(db.String(10), primary_key=True)
    MADATPHONG = db.Column(db.String(10), db.ForeignKey('dat_phong.MADATPHONG'), nullable=False, unique=True)
    MANV = db.Column(db.String(10), db.ForeignKey('nhan_vien.MANV'), nullable=False)
    TIENGIO = db.Column(db.Numeric(18, 2), default=0)
    TIENDICHVU = db.Column(db.Numeric(18, 2), default=0)
    PHANTRAMGIAMGIA = db.Column(db.Numeric(5, 2), default=0)
    SOTIENGIAM = db.Column(db.Numeric(18, 2), default=0)
    TIENVAT = db.Column(db.Numeric(18, 2), default=0)
    TONGTIEN = db.Column(db.Numeric(18, 2), default=0)
    NGAYLAPHD = db.Column(db.DateTime)

    # def __str__(self):
    #     return f"<HoaDon MAHD='{self.MAHD}', MADATPHONG='{self.MADATPHONG}', MANV='{self.MANV}', TIENGIO={self.TIENGIO}, TIENDICHVU={self.TIENDICHVU}, PHANTRAMGIAMGIA={self.PHANTRAMGIAMGIA}, SOTIENGIAM={self.SOTIENGIAM}, TIENVAT={self.TIENVAT}, TONGTIEN={self.TONGTIEN}, NGAYLAPHD='{self.NGAYLAPHD}'>"


class ThemDichVu(db.Model):
    __tablename__ = 'them_dichvu'

    MAHD = db.Column(db.String(10), db.ForeignKey('hoa_don.MAHD'), primary_key=True)
    MADV = db.Column(db.String(10), db.ForeignKey('dich_vu.MADV'), primary_key=True)
    SOLUONG = db.Column(db.Integer, nullable=False)
    GIA = db.Column(db.Numeric(18, 2), nullable=False)

    # def __str__(self):
    #     return f"<ThemDichVu MAHD='{self.MAHD}', MADV='{self.MADV}', SOLUONG={self.SOLUONG}, GIA={self.GIA}>"


class LichSuSD(db.Model):
    __tablename__ = 'lich_su_sd'

    MALICHSU = db.Column(db.String(10), primary_key=True)
    MAKH = db.Column(db.String(10), db.ForeignKey('khach_hang.MAKH'), nullable=False)
    MADATPHONG = db.Column(db.String(10), db.ForeignKey('dat_phong.MADATPHONG'), nullable=False)
    NGAYSUDUNG = db.Column(db.DateTime, nullable=False)
    SOTIENGIAM = db.Column(db.Numeric(18, 2), default=0)

    # def __str__(self):
    #     return f"<LichSuSD MALICHSU='{self.MALICHSU}', MAKH='{self.MAKH}', MADATPHONG='{self.MADATPHONG}', NGAYSUDUNG='{self.NGAYSUDUNG}', SOTIENGIAM={self.SOTIENGIAM}>"

    if __name__ == '__main__':
        with app.app_context():
            test = DatPhong.query.first()
            print(test)
