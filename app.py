from flask import Flask,render_template,request,redirect
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///peserta.db'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#model
class Peserta(db.Model):
    id=db.Column(db.Integer,primary_key = True)
    nama=db.Column(db.String(50))
    alamat=db.Column(db.String(50))
    gender=db.Column(db.String(5))
    umur=db.Column(db.Integer())

    def __repr__(self) -> str:
        return self.nama

@app.route("/")
def welcome_to_budi():
    return{
        "message" : "welcome home"
    }
@app.route("/pendaftar")
def pendaftar():
    list_peserta = Peserta.query.all()
    return render_template("list_pendaftar.html",lp = list_peserta,tgl = date.today())

@app.route("/tambah_pendaftar/<nama>")
def tambah (nama):
    listpendaftar.append(nama)
    return {
        "message" : f"list pendaftar berhasil diupdate : {listpendaftar}"
    }

@app.route("/delete/<nama>")
def delete_pendaftar(nama):
    listpendaftar.remove(nama)
    return{
        "message" : f"Pendaftar berhasil dihapus, menjadi : {listpendaftar}"
    }

if "__main__"==__name__:
    app.run(debug=True, port = 2000)