from flask import Flask,render_template,request,redirect,url_for
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER='static\img'
ALLOWED_EXTENSIONS={'jpg','jpeg','png','HEIC'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///peserta.db'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER   

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#model
class Peserta(db.Model):
    id=db.Column(db.Integer,primary_key = True)
    nama=db.Column(db.String(50))
    alamat=db.Column(db.String(50))
    gender=db.Column(db.String(5))
    umur=db.Column(db.Integer())
    foto=db.Column(db.String(100))

    def __repr__(self) -> str:
        return self.nama

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        foto = request.files['img']

        if foto and allowed_file(foto.filename):
            filename= secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            f_foto = os.path.join('static\img' , filename)
            p=Peserta(nama=f_nama,alamat=f_alamat,gender=f_gender,umur=f_umur,foto=f_foto)
            db.session.add(p)
            db.session.commit()
            return redirect ('/pendaftar')
    
@app.route("/pendaftar/<id>/edit")
def edit_pendaftar(id):
    obj = Peserta.query.filter_by(id=id).first()
    return render_template('edit_pendaftar.html', obj = obj)

@app.route("/pendaftar/<id>/update", methods=['POST'])
def update_pendaftar(id):
    obj = Peserta.query.filter_by(id=id).first()
    f_nama= request.form.get("nama")
    f_alamat= request.form.get("alamat")
    f_gender= request.form.get("gender")
    f_umur= request.form.get("umur")

    obj.nama = f_nama
    obj.alamat = f_alamat
    obj.gender = f_gender
    obj.umur = f_umur
    db.session.add(obj)
    db.session.commit()
    return redirect("/pendaftar")

@app.route("/pendaftar/<id>/delete")
def delete_pendaftar(id):
    obj = Peserta.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect("/pendaftar")
# obj disini bisa  diganti nama var nya

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/load_image')
def image():
    return render_template('load_image.html')   


if "__main__"==__name__:
    app.run(debug=True, port = 2000)