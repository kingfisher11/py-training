from flask import Blueprint
from flask import render_template, request
from einvoicing.invoice.models import invoices
from markupsafe import escape

invoice = Blueprint('invoice', __name__)

@invoice.route("/")
def hello_world():
    module = request.args.get('module', 'Invoice')
    return render_template('index.html', module=module)

@invoice.route("/tambah-invoice/",methods=['GET'])
@invoice.route("/tambah-invoice/<passport>/",methods=['GET'])

@invoice.route("/tambah-invoice>",methods=['GET'])
def create_invoice():
    return "<p>Tambah invoice</p>"

@invoice.route("/simpan-invoice",methods=['POST'])
def save_invoice():
    return "<p>Simpan invoice</p>"

@invoice.route("/selenggara-invoice",methods=['GET', 'POST'])
def manage_invoice():
    return "<p>Selenggara invoice</p>"

@invoice.route("/sunting-invoice/<id>")
def edit_invoice():
    return "<p>Sunting invoice</p>"

@invoice.route("/kemaskini-invoice/<id>")
def update_invoice(id):
    # return "<p>Kemaskini invoice</p> {{id}}"
    return f'Kemaskini invoice {escape(id)}'

@invoice.route("/senarai")
def list_invoice():
    # return "<p>Senarai invoice</p>"
    return render_template('invoice/list.html', invoices=invoices)

@invoice.route("/hapus-invoice/<id>")
def delete_invoice(id):
    return "<p>Kod untuk hapus invoice</p>"+id