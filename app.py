from flask import Flask

app = Flask(__name__)
listpendaftar = []
@app.route("/")
def welcome_to_budi():
    return{
        "message" : "welcome home"
    }
@app.route("/pendaftar")
def pendaftar():
    return {
        "Pendaftar" : listpendaftar
    }

@app.route("/tambah_pendaftar/<nama>")
def tambah (nama):
    listpendaftar.append(nama)
    return {
        "message" : f"list pendaftar berhasil diupdate : {listpendaftar}"
    }


if "__main__"==__name__:
    app.run(debug=True, port = 2000)