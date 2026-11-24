from db import text


type_room_text=text("SELECT DISTINCT LOAIPHONG FROM PHONG_HAT")
booking_history_cus=text("""
SELECT 
    dp.MADATPHONG,
    ph.TENPHONG,
    dp.GIOBATDAU,
    dp.GIOKETTHUC,
    dp.SOLUONGNGUOI,
    dp.TRANGTHAI,
    (SELECT hd.TONGTIEN FROM HOA_DON hd WHERE hd.MADATPHONG = dp.MADATPHONG) AS TONGTIEN
FROM DAT_PHONG dp, PHONG_HAT ph
WHERE dp.MAPHONG = ph.MAPHONG 
  AND dp.MAKH = :makh
ORDER BY dp.MADATPHONG DESC;
""")
#thông tin đặt phòng và tên phòng hát
get_booking_by_id_text = text("""
SELECT dp.MADATPHONG, dp.MAKH, dp.MAPHONG, dp.GIOBATDAU, dp.GIOKETTHUC, dp.SOLUONGNGUOI, dp.TRANGTHAI, ph.TENPHONG, ph.GIATHEOGIO
FROM DAT_PHONG dp, PHONG_HAT ph
WHERE dp.MAPHONG = ph.MAPHONG
  AND dp.MADATPHONG = :madat;
""")

#lấy toàn bộ và đặt bí danh tồnkho
get_all_services_text = text("""
SELECT MADV, TENDV, GIA, LOAIDV, TONKHO
FROM DICH_VU
ORDER BY LOAIDV, TENDV;
""")

#các món đã được gọi
get_ordered_items_text = text("""
SELECT tdv.MAHD, tdv.MADV, tdv.SOLUONG, tdv.GIA, dv.TENDV, dv.LOAIDV
FROM HOA_DON hd, THEM_DICHVU tdv, DICH_VU dv
WHERE hd.MAHD = tdv.MAHD
  AND tdv.MADV = dv.MADV
  AND hd.MADATPHONG = :madat;
""")
get_hoadon_by_booking_text = text("""
SELECT hd.MAHD, hd.TIENDICHVU
FROM HOA_DON hd
WHERE hd.MADATPHONG = (
    SELECT dp.MADATPHONG 
    FROM DAT_PHONG dp 
    WHERE dp.MADATPHONG = :madat
);
""")
#các món đã đc thêm
get_them_dichvu_item_text = text("""
SELECT MAHD, MADV, SOLUONG, GIA
FROM THEM_DICHVU
WHERE MAHD = :mahd AND MADV = :madv;
""")


get_status_room_text= text("""
SELECT DISTINCT TRANGTHAI
FROM PHONG_HAT
""")

get_booking_reception_text = text("""
SELECT ph.TENPHONG, kh.TENKH, dp.GIOBATDAU, dp.GIOKETTHUC, dp.SOLUONGNGUOI, dp.TRANGTHAI, dp.MADATPHONG
FROM DAT_PHONG dp, PHONG_HAT ph, KHACH_HANG kh
WHERE dp.MAKH = kh.MAKH AND dp.MAPHONG = ph.MAPHONG
ORDER BY dp.MADATPHONG DESC
""")

# khi toiws giờ thì sẽ tự động cập nhật trạng thái
auto_update_booking_status_text = text("""
UPDATE DAT_PHONG 
SET TRANGTHAI = 'InUse' 
WHERE TRANGTHAI = 'Booked' AND GIOBATDAU <= :now
""")

#nếu inuse thì sẽ chuyển sang occupied
auto_update_room_status_text = text("""
UPDATE PHONG_HAT 
SET TRANGTHAI = 'Occupied' 
WHERE MAPHONG IN (
    SELECT MAPHONG 
    FROM DAT_PHONG 
    WHERE TRANGTHAI = 'InUse'
) AND TRANGTHAI = 'Available'
""")