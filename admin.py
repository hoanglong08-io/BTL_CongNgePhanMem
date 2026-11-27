from flask import abort, redirect, request
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from db import app, db
from model import DichVu, HoaDon




# 1. Áp dụng cho trang chủ Admin (AdminIndexView)
class MyAdminIndexView(AdminIndexView):

    @expose("/")
    def index(self):
        return self.render("admin/index.html")
   


# 2. Áp dụng cho các bảng Model (CRUD Dịch vụ)
class DichVuView(ModelView):
    column_list = ["MADV", "TENDV", "LOAIDV", "GIA", "TONKHO"]
    column_searchable_list = ["TENDV", "LOAIDV"]
    column_filters = ["LOAIDV", "GIA"]


# 3. Áp dụng cho trang Thống kê (BaseView)
class MyStatView(BaseView):

    @expose("/")
    def index(self):
        # ... Giữ nguyên logic tính toán thống kê của bạn ở đây ...
        return self.render("admin/stats.html")
    def is_accessible(self)->bool:
        return current_user.is_authenticated and current_user.role in ['STAFF', 'OWNER']


# 4. Trang Đăng xuất (Chỉ Admin mới chạy được)
class MyLogoutView(BaseView):

    @expose("/")
    def index(self):
        logout_user()
        return redirect("/")  # Đăng xuất xong về trang chủ chính
    def is_accessible(self)->bool:
        return current_user.is_authenticated and current_user.role in ['STAFF', 'OWNER']

# Khởi tạo Admin
admin = Admin(
    app=app,
    name="Karaoke Room Booking",
    url="/admin",  # Đường dẫn Admin
    index_view=MyAdminIndexView(),
    
)

admin.add_view(DichVuView(DichVu, db.session, name="Food and drink"))
admin.add_view(MyStatView(name="Analystic"))
admin.add_view(MyLogoutView(name="Log out"))