from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World! - KPTM HQ</p>"

@app.route("/selenggara-pengguna")
def manage_user():
    return "<p>Selenggara Pengguna</p>"

@app.route("/senarai-pengguna")
def list_user():
    return "<p>Senarai Pengguna</p>"

@app.route("/sunting-pengguna")
def edit_user():
    return "<p>Sunting Pengguna</p>"

@app.route("/kemaskini-pengguna/<id>")
def update_user():
    # return "<p>Kemaskini Pengguna</p> {{id}}"
    return "<p>Kemaskini Pengguna</p> {{id}}"

@app.route("/hapus-pengguna")
def delete_user():
    return "<p>Hapus Pengguna</p>"

@app.route("/tambah-pengguna/<passport>")
def add_user(passport='0'):
    return "<p>Tambah Pengguna</p>"+passport

@app.route("/simpan-pengguna")
def save_user():
    return "<p>Simpan Pengguna</p>"