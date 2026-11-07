from flask import Flask, render_template, request, session, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
import dao



app = Flask(__name__)
app.secret_key = 'karaoke_secret_key'


@app.route("/")
def home():
    rooms = dao.load_room()
    types = dao.load_room()
    return render_template("index.html", rooms=rooms)


@app.route("/login", methods=['GET','POST'])
def login():
    r = request.method
    if r == 'GET':
        return render_template("login.html")
    if r == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username, password)
        if user:
            # lưu lại phiên làm việc
            session['username'] = username
            session['name'] = user[0]
            session['role'] = user[1]
            print(session)
            return redirect('/')
        
        else:
            flash ('Tên đăng nhập hoặc mật khẩu không chính xác!')
            return redirect('/login')
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', method=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        r = request.form
        user = r.get('name')
        phone = r.get('phone')
        password = r.get('password')
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True, port=4300)