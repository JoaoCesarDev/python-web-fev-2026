<<<<<<< HEAD
import os
from flask import Flask, render_template, g, request, redirect, url_for, redirect,abort,session,flash
from dotenv import load_dotenv

import sqlite3

DATABASE = "banco.db"
SECRET_KEY = "1234"

load_dotenv()

app = Flask(__name__)

app.config.from_object(__name__)

def conectar():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = conectar()

@app.teardown_request
def teardown_request(f):
    g.db.close()

@app.route('/')
def exibir_posts():
    sql = "SELECT id,titulo, texto, data_criacao from posts ORDER BY id ASC"
    resultado = g.db.execute(sql)
    posts = []

    for id, titulo, texto, data_criacao in resultado.fetchall():
        posts.append({
            "id": str(id),
            "titulo": titulo,
            "texto": texto,
            "data_criacao": data_criacao
        })

    return render_template('exibir_posts.html', post = posts) 

@app.route('/login', methods=["GET", "POST"])
def login():
    erro = None
    if(request.method == "POST"):
        if(request.form["username"] != "admin" or request.form["password"] != "jcbest"):
            erro = "Usuário ou senha inválidos"
        else:
            session["logged_in"] = True
            flash("Login realizado com sucesso!  " + request.form["username"])
            return redirect(url_for("exibir_posts"))
    return render_template("login.html", erro = erro)

@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    flash("Logout realizado com sucesso!")
    return redirect(url_for("exibir_posts"))

@app.route('/inserir', methods=["GET", "POST"])
def inserir():
    if(not session.get("logged_in")):
        abort(401)
    titulo = request.form["titulo"]
    texto = request.form["texto"]
    sql = "INSERT INTO posts (titulo, texto) VALUES (?, ?)"
    g.db.execute(sql, (titulo, texto))
    g.db.commit()
    flash("Post inserido com sucesso!")
    return redirect(url_for("exibir_posts"))

@app.route('/deletar/<int:id>')
def deletar(id):
    if(not session.get("logged_in")):
        abort(401)
    sql = "DELETE FROM posts WHERE id = ?"
    g.db.execute(sql, (id,))
    g.db.commit()
    flash("Post deletado com sucesso!")
    return redirect(url_for("exibir_posts"))


if __name__ == '__main__':
    app.run(port=os.getenv("FLASK_PORT"),
            debug=os.getenv("FLASK_DEBUG"),
            host=os.getenv("FLASK_HOST"))
=======
from flask import Flask

app = Flask(__name__)

@app.route('/')

def home():
    return "Hello, World!"
>>>>>>> 25b93fcb0b10154ca80cd5c2f563ffee667efb07
