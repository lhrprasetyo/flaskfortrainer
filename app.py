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

@app.route("/tambah_pendaftar")
def form_tambah():
    return render_template ('tambah_pendaftar.html')

@app.route("/tambah_pendaftar/save", methods =['POST']) 
def tambah ():
    if request.method == 'POST':
        # membuat object peserta 
        f_nama = request.form.get("nama")
        f_alamat = request.form.get("alamat")
        f_gender = request.form.get("gender")
        f_umur = request.form.get("umur")

    p=Peserta(nama=f_nama,alamat=f_alamat,gender=f_gender,umur=f_umur)
    db.session.add(p)
    db.session.commit()
    return redirect ('/pendaftar')
    

@app.route("/delete/<nama>")
def delete_pendaftar(nama):
    listpendaftar.remove(nama)
    return{
        "message" : f"Pendaftar berhasil dihapus, menjadi : {listpendaftar}"
    }

@app.route("/home/<nama>")
def home(nama):
    nama=nama
    return render_template ('home.html', nama = nama)


if "__main__"==__name__:
    app.run(debug=True, port = 2000)