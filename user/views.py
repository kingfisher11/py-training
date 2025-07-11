from flask import Blueprint
from markupsafe import escape
# from einvoicing import db
from flask import render_template, request, flash, session, redirect, url_for
from einvoicing.user.models import User, RegistrationForm, LoginForm
from flask import Blueprint, jsonify
from einvoicing import db

user = Blueprint('user', __name__)

@user.route("/")
def hello_world():
    return "<p>Training Day - This is KPTM HQ </p>"

@user.route("/tambah-pengguna/",methods=['GET'])
def create_user():
    return "<p>Tambah Pengguna</p>"

@user.route("/simpan-pengguna",methods=['POST'])
def save_user():
    return "<p>Simpan Pengguna</p>"

@user.route("/list")
def list_user():
    # return "<p>Senarai Pengguna</p>"
    page = request.args.get('page', 1, type=int)
    per_page = 10
    paginated_users = User.query.order_by(User.id).paginate(page=page, per_page=per_page)
    return render_template('user/list.html', users=paginated_users)
    # users = User.query.all()
    # return render_template('user/list.html', users=users)
    # res = []
    # for u in users:
    #     res.append({
    #         'id': u.id,
    #         'name': u.name,
    #         'email': u.email
    #     })

    # return jsonify(res)

@user.route("/hapus-pengguna/<id>")
def delete_user(id):
    return "<p>Kod untuk hapus Pengguna</p>"+id

