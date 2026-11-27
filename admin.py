from flask import abort, redirect, request
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from db import app, db
from model import DichVu, HoaDon


class MyAdminIndexView(AdminIndexView):

    @expose("/")
    def index(self):
        return self.render("admin/index.html")
   


class DichVuView(ModelView):
    column_list = ["MADV", "TENDV", "LOAIDV", "GIA", "TONKHO"]
    column_searchable_list = ["TENDV", "LOAIDV"]
    column_filters = ["LOAIDV", "GIA"]
    def is_accessible(self)->bool:
        return current_user.is_authenticated and current_user.role in ['STAFF', 'OWNER'] 

class MyStatView(BaseView):

    @expose("/")
    def index(self):
        return self.render("admin/stats.html")
    def is_accessible(self)->bool:
        return current_user.is_authenticated and current_user.role == 'OWNER'


class MyLogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

# Khởi tạo Admin
admin = Admin(
    app=app,
    name="Karaoke Room Booking",
    url="/admin",  # Đường dẫn Admin
    index_view=MyAdminIndexView(),
    
)

admin.add_view(DichVuView(DichVu, db.session, name="Food and drink"))
admin.add_view(MyStatView(name="Analystic"))
admin.add_view(MyLogoutView(name="Đăng xuất"))