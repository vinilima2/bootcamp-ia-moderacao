from flask import flash, request, render_template, redirect, session
from datetime import datetime
from dotenv import load_dotenv
import uuid
import bcrypt

from src.dbmanager import DBManager
from main import app
from src.ia import analisar_comentario

DATABASE = DBManager("database/db.db")

load_dotenv()

@app.route("/")
def main():
    if "name" not in session:
        return redirect("/login")

    posts = DATABASE.raw_sql("""
        SELECT p.*, u.nome_usuario 
        FROM Post AS p
        JOIN Usuario AS u ON p.usuario_id = u.usuario_id
        ORDER BY p.data_criacao DESC
    """).json

    for post in posts:
        post_id = post["post_id"]
        post["respostas"] = DATABASE.raw_sql(f"""
            SELECT r.*, u.nome_usuario 
            FROM Resposta AS r
            JOIN Usuario AS u ON r.usuario_id = u.usuario_id
            WHERE r.post_id = '{post_id}'
            ORDER BY r.data_criacao DESC
        """).json

    return render_template("index.html", posts=posts, usuario=session["name"])

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("cadastro.html")

    nome_usuario = request.form.get("usuario")

    # Verifica se o novo nome de usuário está disponível
    if DATABASE.value_in_column_exists("Usuario", "nome_usuario", nome_usuario) == "True":
        flash('Atenção, O nome de usuário inserido já existe.', 'warning')
        return redirect("/registro")

    senha = request.form.get("senha")
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    datahora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    DATABASE.insert_all("Usuario", [
        f"'{uuid.uuid4()}'",
        f"'{nome_usuario}'",
        f"'{senha_hash}'",
        f"'{datahora}'"
    ])
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    nome_usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    result = DATABASE.raw_sql(f"""
        SELECT senha FROM Usuario 
        WHERE nome_usuario = '{nome_usuario}'
    """).json

    if result and bcrypt.checkpw(senha.encode(), result[0]["senha"].encode()):
        session["name"] = nome_usuario
        return redirect("/")
    
    flash('Atenção, Usuário ou senha inválidos.', 'warning')
    return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/post/novo", methods=["POST"])
def novo_post():
    if "name" not in session:
        return redirect("/login")

    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")
    usuario_id = get_usuario_id(session["name"])
    datahora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    texto_avaliado = analisar_comentario(titulo + ": " + descricao)

    if texto_avaliado['erro'] == True:
       flash(texto_avaliado['motivo'], 'error')
       return redirect("/")

    bloqueado = not texto_avaliado['aprovado']

    DATABASE.insert_all("Post", [
        f"'{uuid.uuid4()}'",
        f"'{titulo}'",
        f"'{descricao}'",
        f"'{datahora}'",
        f"'{usuario_id}'",
        bloqueado and "1" or "0"
    ])

    if bloqueado:
        flash('Post bloqueado, por ferir diretrizes da comunidade.', 'error')

    return redirect("/")

@app.route("/resposta/novo", methods=["POST"])
def nova_resposta():
    if "name" not in session:
        return redirect("/login")

    descricao = request.form.get("descricao")
    post_id = request.form.get("post_id")
    usuario_id = get_usuario_id(session["name"])
    datahora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    texto_avaliado = analisar_comentario(descricao)

    if texto_avaliado['erro'] == True:
       flash(texto_avaliado['motivo'], 'error')
       return redirect("/")
       
    bloqueado = not texto_avaliado['aprovado']

    DATABASE.insert_all("Resposta", [
        f"'{uuid.uuid4()}'",
        f"'{post_id}'",
        f"'{descricao}'",
        f"'{usuario_id}'",
        f"'{datahora}'",
        bloqueado and "1" or "0"
    ])

    if bloqueado:
        flash('Resposta bloqueada, por ferir diretrizes da comunidade.', 'error')
    
    return redirect("/")

def get_usuario_id(nome_usuario):
    result = DATABASE.raw_sql(f"SELECT usuario_id FROM Usuario WHERE nome_usuario = '{nome_usuario}'").json
    return result[0]["usuario_id"] if result else None