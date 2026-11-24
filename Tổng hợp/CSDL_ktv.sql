CREATE DATABASE IF NOT EXISTS karaokedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE karaokedb;

DROP TABLE IF EXISTS LICH_SU_SD;
DROP TABLE IF EXISTS THEM_DICHVU;
DROP TABLE IF EXISTS HOA_DON;
DROP TABLE IF EXISTS DICH_VU;
DROP TABLE IF EXISTS DAT_PHONG;
DROP TABLE IF EXISTS PHONG_HAT;
DROP TABLE IF EXISTS NHAN_VIEN;
DROP TABLE IF EXISTS KHACH_HANG;

SET @today = CURDATE();
SET @this_month = @today - INTERVAL (DAYOFMONTH(@today) - 1) DAY;


-- =========================================
-- 2. BANG KHACH HANG
-- =========================================

CREATE TABLE KHACH_HANG (
    MAKH INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    TENKH NVARCHAR(100) NOT NULL,
    SDT VARCHAR(15) NOT NULL UNIQUE,
    USERNAME VARCHAR(50) NOT NULL UNIQUE,
    PASSWORD VARCHAR(255)
);


-- =========================================
-- 3. BANG NHAN VIEN
-- =========================================

CREATE TABLE NHAN_VIEN (
    MANV INT AUTO_INCREMENT PRIMARY KEY,
    TENNV NVARCHAR(100) NOT NULL,
    USERNAME VARCHAR(50) UNIQUE,
    PASSWORD VARCHAR(255),
    ROLE NVARCHAR(30)
);


-- =========================================
-- 4. BANG PHONG HAT
-- =========================================

CREATE TABLE PHONG_HAT (
    MAPHONG INT AUTO_INCREMENT PRIMARY KEY,
    TENPHONG NVARCHAR(50),
    LOAIPHONG NVARCHAR(50),
    SUCCHUA INT NOT NULL,
    GIATHEOGIO DECIMAL(18,2) NOT NULL,
    TRANGTHAI NVARCHAR(30),

    CHECK (SUCCHUA > 0),
    CHECK (GIATHEOGIO >= 0)
);


-- =========================================
-- 5. BANG DAT PHONG
-- =========================================

CREATE TABLE DAT_PHONG (
    MADATPHONG INT AUTO_INCREMENT PRIMARY KEY,
    MAKH INT NOT NULL,
    MAPHONG INT NOT NULL, 
    GIOBATDAU DATETIME NOT NULL,
    GIOKETTHUC DATETIME NOT NULL,
    SOLUONGNGUOI INT NOT NULL,
    TRANGTHAI NVARCHAR(30),
   
    
    FOREIGN KEY (MAKH) REFERENCES KHACH_HANG(MAKH),
    FOREIGN KEY (MAPHONG) REFERENCES PHONG_HAT(MAPHONG),

    CHECK (GIOKETTHUC > GIOBATDAU),
    CHECK (SOLUONGNGUOI > 0 AND SOLUONGNGUOI <= 15)
);


-- =========================================
-- 6. BANG DICH VU
-- =========================================

CREATE TABLE DICH_VU (
    MADV INT AUTO_INCREMENT PRIMARY KEY,
    TENDV NVARCHAR(100) NOT NULL,
    GIA DECIMAL(18,2) NOT NULL,
    LOAIDV NVARCHAR(50)
);


-- =========================================
-- 7. BANG HOA DON
-- =========================================

CREATE TABLE HOA_DON (
    MAHD INT AUTO_INCREMENT PRIMARY KEY,
    MADATPHONG INT NOT NULL UNIQUE,
    MANV INT NOT NULL,
    TIENGIO DECIMAL(18,2) DEFAULT 0,
    TIENDICHVU DECIMAL(18,2) DEFAULT 0,
    PHANTRAMGIAMGIA DECIMAL(5,2) DEFAULT 0,
    SOTIENGIAM DECIMAL(18,2) DEFAULT 0,
    TIENVAT DECIMAL(18,2) DEFAULT 0,
    TONGTIEN DECIMAL(18,2) DEFAULT 0,
    NGAYLAPHD DATETIME,

    FOREIGN KEY (MADATPHONG) REFERENCES DAT_PHONG(MADATPHONG),
    FOREIGN KEY (MANV) REFERENCES NHAN_VIEN(MANV)
);


-- =========================================
-- 8. BANG THEM DICH VU
-- =========================================

CREATE TABLE THEM_DICHVU (
    MAHD INT,
    MADV INT,
    SOLUONG INT NOT NULL,
    GIA DECIMAL(18,2) NOT NULL,

    PRIMARY KEY (MAHD, MADV),
    FOREIGN KEY (MAHD) REFERENCES HOA_DON(MAHD),
    FOREIGN KEY (MADV) REFERENCES DICH_VU(MADV),

    CHECK (SOLUONG > 0),
    CHECK (GIA >= 0)
);


-- =========================================
-- 9. BANG LICH SU SU DUNG
-- =========================================

CREATE TABLE LICH_SU_SD (
    MALICHSU INT AUTO_INCREMENT PRIMARY KEY,
    MAKH INT NOT NULL,
    MADATPHONG INT NOT NULL,
    NGAYSUDUNG DATETIME NOT NULL,
    SOTIENGIAM DECIMAL(18,2) DEFAULT 0,

    FOREIGN KEY (MAKH) REFERENCES KHACH_HANG(MAKH),
    FOREIGN KEY (MADATPHONG) REFERENCES DAT_PHONG(MADATPHONG)
);


-- =========================================
-- INSERT DATA (ĐÃ CHỈNH SỬA KIỂU INT KHỚP VỚI CSDL)
-- =========================================

INSERT INTO KHACH_HANG (MAKH, TENKH, SDT, USERNAME, PASSWORD) VALUES
  (1, 'Nguyen Van An', '0901000001', 'customer', 'f4ad231214cb99a985dff0f056a36242'),
  (2, 'Tran Thi Binh', '0901000002', 'binh', '08413b9c876b4976053e6c3300708141'),
  (3, 'Le Hoang Cuong', '0901000003', 'cuong', '188c979b22d6ddcfcaf1ed12e4378028'),
  (4, 'Pham Thi Dung', '0901000004', 'dung', 'd30ef5569a0a3f315e0b91b0a129ae9f'),
  (5, 'Dang Thu Ha', '0901000007', 'thuha', 'da3b82b41a35ae89c242a375199f01e0');

INSERT INTO NHAN_VIEN (MANV, TENNV, USERNAME, PASSWORD, ROLE) VALUES
  (1, 'Nguyen Minh Chau', 'owner', '5be057accb25758101fa5eadbbd79503', 'OWNER'),
  (2, 'Le Thu Lan', 'staff', 'de9bf5643eabf80f4a56fda3bbb84483', 'STAFF'),
  (3, 'Pham Quoc Huy', 'staff2', '3b615550a12aafc90faeedf650fa03c9', 'STAFF');

INSERT INTO PHONG_HAT (MAPHONG, TENPHONG, LOAIPHONG, SUCCHUA, GIATHEOGIO, TRANGTHAI) VALUES
  (1, 'Room 101', 'Standard', 6, 150000, 'Available'),
  (2, 'Room 102', 'Standard', 6, 150000, 'Available'),
  (3, 'Room 103', 'Standard', 8, 180000, 'Maintenance'),
  (4, 'Room 201', 'VIP', 10, 300000, 'Available'),
  (5, 'Room 202', 'VIP', 10, 300000, 'Occupied'),
  (6, 'Room 301', 'Party', 15, 500000, 'Available'),
  (7, 'Room 302', 'Party', 12, 420000, 'Available');

INSERT INTO DICH_VU (MADV, TENDV, GIA, LOAIDV) VALUES
  (1, 'Tiger beer', 25000, 'Drink'),
  (2, 'Coca-Cola', 20000, 'Drink'),
  (3, 'Mineral water', 10000, 'Drink'),
  (4, 'Whisky bottle', 650000, 'Drink'),
  (5, 'Fruit platter', 120000, 'Food'),
  (6, 'Dried squid', 90000, 'Food'),
  (7, 'French fries', 60000, 'Food'),
  (8, 'Popcorn', 40000, 'Food');

INSERT INTO DAT_PHONG (MADATPHONG, MAKH, MAPHONG, GIOBATDAU, GIOKETTHUC, SOLUONGNGUOI, TRANGTHAI) VALUES
  (1, 1, 1, TIMESTAMP(@this_month + INTERVAL 0 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 0 DAY, '21:00:00'), 3, 'Completed'),
  (2, 1, 4, TIMESTAMP(@this_month + INTERVAL 1 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 1 DAY, '21:00:00'), 4, 'Completed'),
  (3, 1, 1, TIMESTAMP(@this_month + INTERVAL 2 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 2 DAY, '21:00:00'), 5, 'Completed'),
  (4, 1, 4, TIMESTAMP(@this_month + INTERVAL 3 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 3 DAY, '21:00:00'), 6, 'Completed'),
  (5, 1, 1, TIMESTAMP(@this_month + INTERVAL 4 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 4 DAY, '21:00:00'), 3, 'Completed'),
  (6, 1, 4, TIMESTAMP(@this_month + INTERVAL 5 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 5 DAY, '21:00:00'), 4, 'Completed'),
  (7, 1, 1, TIMESTAMP(@this_month + INTERVAL 6 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 6 DAY, '21:00:00'), 5, 'Completed'),
  (8, 1, 4, TIMESTAMP(@this_month + INTERVAL 7 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 7 DAY, '21:00:00'), 6, 'Completed'),
  (9, 3, 1, TIMESTAMP(@this_month + INTERVAL 8 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 8 DAY, '21:00:00'), 3, 'Completed'),
  (10, 3, 4, TIMESTAMP(@this_month + INTERVAL 9 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 9 DAY, '21:00:00'), 4, 'Completed'),
  (11, 2, 1, TIMESTAMP(@this_month + INTERVAL 10 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 10 DAY, '21:00:00'), 5, 'Completed'),
  (12, 1, 4, TIMESTAMP(@this_month + INTERVAL 11 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 11 DAY, '21:00:00'), 6, 'Completed'),
  (13, 3, 1, TIMESTAMP(@this_month + INTERVAL 0 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 0 DAY, '21:00:00'), 3, 'Completed'),
  (14, 1, 4, TIMESTAMP(@this_month + INTERVAL 1 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 1 DAY, '21:00:00'), 4, 'Completed'),
  (15, 1, 1, TIMESTAMP(@this_month + INTERVAL 2 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 2 DAY, '21:00:00'), 5, 'Completed'),
  (16, 2, 4, TIMESTAMP(@this_month + INTERVAL 3 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 3 DAY, '21:00:00'), 6, 'Completed'),
  (17, 1, 1, TIMESTAMP(@this_month + INTERVAL 4 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 4 DAY, '21:00:00'), 3, 'Completed'),
  (18, 5, 4, TIMESTAMP(@this_month + INTERVAL 5 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 5 DAY, '21:00:00'), 4, 'Completed'),
  (19, 1, 1, TIMESTAMP(@this_month + INTERVAL 6 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 6 DAY, '21:00:00'), 5, 'Completed'),
  (20, 5, 4, TIMESTAMP(@this_month + INTERVAL 7 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 7 DAY, '21:00:00'), 6, 'Completed'),
  (21, 5, 1, TIMESTAMP(@this_month + INTERVAL 8 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 8 DAY, '21:00:00'), 3, 'Completed'),
  (22, 4, 4, TIMESTAMP(@this_month + INTERVAL 9 DAY, '19:00:00'), TIMESTAMP(@this_month + INTERVAL 9 DAY, '21:00:00'), 4, 'Completed'),
  (23, 3, 7, TIMESTAMP(@today - INTERVAL 1 DAY, '19:30:00'), TIMESTAMP(@today - INTERVAL 1 DAY, '21:00:00'), 3, 'Completed');

INSERT INTO HOA_DON (MAHD, MADATPHONG, MANV, TIENGIO, TIENDICHVU, PHANTRAMGIAMGIA, SOTIENGIAM, TIENVAT, TONGTIEN, NGAYLAPHD) VALUES
  (1, 1, 2, 300000.00, 0.00, 0.00, 0.00, 30000.00, 330000.00, NOW()),
  (2, 2, 3, 600000.00, 110000.00, 0.00, 0.00, 71000.00, 781000.00, NOW()),
  (3, 3, 2, 300000.00, 160000.00, 0.00, 0.00, 46000.00, 506000.00, NOW()),
  (4, 4, 3, 600000.00, 0.00, 0.00, 0.00, 60000.00, 660000.00, NOW()),
  (5, 5, 2, 300000.00, 110000.00, 0.00, 0.00, 41000.00, 451000.00, NOW()),
  (6, 6, 3, 600000.00, 160000.00, 0.00, 0.00, 76000.00, 836000.00, NOW()),
  (7, 7, 2, 300000.00, 0.00, 0.00, 0.00, 30000.00, 330000.00, NOW()),
  (8, 8, 3, 600000.00, 110000.00, 0.00, 0.00, 71000.00, 781000.00, NOW()),
  (9, 9, 2, 300000.00, 160000.00, 0.00, 0.00, 46000.00, 506000.00, NOW()),
  (10, 10, 3, 600000.00, 0.00, 0.00, 0.00, 60000.00, 660000.00, NOW()),
  (11, 11, 2, 300000.00, 110000.00, 5.00, 20500.00, 38950.00, 428450.00, NOW()),
  (12, 12, 3, 600000.00, 160000.00, 5.00, 38000.00, 72200.00, 794200.00, NOW()),
  (13, 13, 2, 300000.00, 0.00, 0.00, 0.00, 30000.00, 330000.00, NOW()),
  (14, 14, 3, 600000.00, 110000.00, 0.00, 0.00, 71000.00, 781000.00, NOW()),
  (15, 15, 2, 300000.00, 160000.00, 0.00, 0.00, 46000.00, 506000.00, NOW()),
  (16, 16, 3, 600000.00, 0.00, 0.00, 0.00, 60000.00, 660000.00, NOW()),
  (17, 17, 2, 300000.00, 110000.00, 0.00, 0.00, 41000.00, 451000.00, NOW()),
  (18, 18, 3, 600000.00, 160000.00, 0.00, 0.00, 76000.00, 836000.00, NOW()),
  (19, 19, 2, 300000.00, 0.00, 0.00, 0.00, 30000.00, 330000.00, NOW()),
  (20, 20, 3, 600000.00, 110000.00, 0.00, 0.00, 71000.00, 781000.00, NOW()),
  (21, 21, 2, 300000.00, 160000.00, 0.00, 0.00, 46000.00, 506000.00, NOW()),
  (22, 22, 3, 600000.00, 0.00, 0.00, 0.00, 60000.00, 660000.00, NOW()),
  (23, 23, 2, 630000.00, 730000.00, 0.00, 0.00, 136000.00, 1496000.00, NOW());

INSERT INTO THEM_DICHVU (MAHD, MADV, SOLUONG, GIA) VALUES
  (2, 1, 2, 25000),
  (2, 7, 1, 60000),
  (3, 5, 1, 120000),
  (3, 2, 2, 20000),
  (5, 1, 2, 25000),
  (5, 7, 1, 60000),
  (6, 5, 1, 120000),
  (6, 2, 2, 20000),
  (8, 1, 2, 25000),
  (8, 7, 1, 60000),
  (9, 5, 1, 120000),
  (9, 2, 2, 20000),
  (11, 1, 2, 25000),
  (11, 7, 1, 60000),
  (12, 5, 1, 120000),
  (12, 2, 2, 20000),
  (14, 1, 2, 25000),
  (14, 7, 1, 60000),
  (15, 5, 1, 120000),
  (15, 2, 2, 20000),
  (17, 1, 2, 25000),
  (17, 7, 1, 60000),
  (18, 5, 1, 120000),
  (18, 2, 2, 20000),
  (20, 1, 2, 25000),
  (20, 7, 1, 60000),
  (21, 5, 1, 120000),
  (21, 2, 2, 20000),
  (23, 3, 3, 10000),
  (23, 1, 2, 25000),
  (23, 4, 1, 650000);

INSERT INTO LICH_SU_SD (MALICHSU, MAKH, MADATPHONG, NGAYSUDUNG, SOTIENGIAM) VALUES
  (1, 1, 11, TIMESTAMP(@this_month + INTERVAL 10 DAY, '21:00:00'), 20500.00),
  (2, 1, 12, TIMESTAMP(@this_month + INTERVAL 11 DAY, '21:00:00'), 38000.00);