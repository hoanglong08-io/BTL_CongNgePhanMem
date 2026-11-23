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
ORDER BY dp.GIOBATDAU DESC;
""")
#thông tin đặt phòng và tên phòng hát
get_booking_by_id_text = text("""
SELECT dp.MADATPHONG, dp.MAKH, dp.MAPHONG, dp.GIOBATDAU, dp.GIOKETTHUC, dp.SOLUONGNGUOI, dp.TRANGTHAI, ph.TENPHONG
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
    -- BƯỚC 1 (TRUY VẤN LỒNG): XÁC NHẬN MÃ ĐẶT PHÒNG TỒN TẠI TRONG BẢNG DAT_PHONG
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
