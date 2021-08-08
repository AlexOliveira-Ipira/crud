from flask import Flask , request, jsonify, json
from flask import redirect, render_template, session, url_for,flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'docker'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), nullable = False)
    nome = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), unique = True , nullable = False)
    confemail = db.Column(db.String(120), nullable = False)
    senha = db.Column(db.String(30), nullable = False)
    confsenha = db.Column(db.String(30), nullable = False)
    datacadastro = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    datavalidade = db.Column(db.DateTime(), nullable = False, default=datetime.utcnow)
   

    def __init__(self, usuario, nome, email, confemail, senha , confsenha):
        self.usuario = usuario
        self.nome = nome
        self.email = email
        self.confemail = confemail
        self.senha = senha
        self.confsenha = confsenha
        


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/cad', methods=['POST', 'GET'])
def cad():
    usuario = request.values.get('usuario')
    if usuario:
        usuario = request.values.get('usuario')
        name = request.values.get('nome')
        email = request.values.get('email')
        confemail = request.values.get('confemail')
        senha = request.values.get('senha')
        confsenha = request.values.get('confsenha')
    
      

        newuser = Users(usuario, name, email, confemail, senha, confsenha)
        db.session.add(newuser)
        db.session.commit()

        return redirect(url_for('view'))
    return render_template('cad.html')


@app.route("/update/<usuario>" , methods=['POST', 'GET'])
def update(usuario):
    upusuario = Users.query.filter_by(usuario=usuario).first()
    if request.method == "POST":

        newname = request.values.get('nome')
        newnemail = request.values.get('email')

        upusuario.usuario = upusuario.usuario
        upusuario.nome = newname
        upusuario.email = newnemail

        db.session.commit()
        return redirect(url_for('view'))
    return render_template('update.html', usuario = upusuario)
        

@app.route('/logout')
def logout():
    session.pop('usuario', None)   
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/view')
def view():
    dadoscad = Users.query.limit(5).all()
    return render_template('view.html', dados=dadoscad)

@app.route('/delete/<usuario>', methods=['GET'])
def delete(usuario):
    deluser = Users.query.filter_by(usuario=usuario).first()

    db.session.delete(deluser)
    db.session.commit()
    dadoscad = Users.query.limit(5).all()
    return render_template('view.html', dados=dadoscad)
   

   
if __name__ =='__main__':
    db.create_all()
    app.run(debug=True , port=8880)