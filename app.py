from flask import Flask, render_template, request
import dao

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/")
def home():
    rooms = dao.load_room()
    return render_template("index.html", rooms=rooms)
@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)