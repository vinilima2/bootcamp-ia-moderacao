from dbmanager import DBManager
from main import app
from datetime import datetime
import uuid
import bcrypt
from flask import redirect, render_template, request, session


DATABASE = DBManager("database/db.db")


@app.route("/")
def main():
    if not session.get("name"):
        return redirect("/login")
    DATABASE.get_all("Tag")
    posts = DATABASE.raw_sql(
        """
    SELECT c.*, u.nome_usuario FROM Post AS c
	JOIN Usuario AS u ON c.usuario_id = u.usuario_id
    ORDER BY c.data_criacao DESC
    """
    ).json

    for post in posts:
        post["respostas"] = DATABASE.raw_sql(
            """
    SELECT r.*, u.nome_usuario FROM Resposta AS r
	JOIN Usuario AS u ON r.usuario_id = u.usuario_id
    WHERE r.post_id = {post_id} 
    ORDER BY r.data_criacao DESC
    """.format(
                post_id="'" + post["post_id"] + "'"
            )
        ).json

    usuario = session.get("name")
    print(posts)
    return render_template("index.html", posts=posts, usuario=usuario)


@app.route("/analyse", methods=["POST"])
def analyse():
    id_msg, msg = request.get_json().values()
    return id_msg + " " + msg


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("cadastro.html")
    nome_usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    datahora_atual = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    DATABASE.insert_all(
        "Usuario",
        [
            "'" + str(uuid.uuid4()) + "'",
            "'" + nome_usuario + "'",
            "'" + senha_hash + "'",
            "'" + str(datahora_atual) + "'",
        ],
    )
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    nome_usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    usuario = DATABASE.raw_sql(
        """
    SELECT u.senha FROM Usuario u
	WHERE u.nome_usuario = {nome_usuario}
    """.format(
            nome_usuario="'" + nome_usuario + "'"
        )
    )
    if usuario.json != [] and bcrypt.checkpw(
        bytes(senha, "utf-8"), bytes(usuario.json[0]["senha"], "utf-8")
    ):
        session["name"] = nome_usuario
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/post/novo", methods=["POST"])
def novo_post():
    descricao = request.form.get("descricao")
    titulo = request.form.get("titulo")
    nome_usuario = session.get("name")

    print(nome_usuario)
    usuario = DATABASE.raw_sql(
        """
    SELECT u.usuario_id FROM Usuario u
	WHERE u.nome_usuario = {nome_usuario}
    """.format(
            nome_usuario="'" + nome_usuario + "'"
        )
    ).json[0]["usuario_id"]

    datahora_atual = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    DATABASE.insert_all(
        "Post",
        [
            "'" + str(uuid.uuid4()) + "'",
            "'" + titulo + "'",
            "'" + descricao + "'",
            "'" + str(datahora_atual) + "'",
            "'" + usuario + "'",
            str(0),
        ],
    )
    return redirect("/")


@app.route("/resposta/novo", methods=["POST"])
def nova_resposta():
    descricao = request.form.get("descricao")
    post_id = request.form.get("post_id")
    nome_usuario = session.get("name")

    print(nome_usuario)
    usuario = DATABASE.raw_sql(
        """
    SELECT u.usuario_id FROM Usuario u
	WHERE u.nome_usuario = {nome_usuario}
    """.format(
            nome_usuario="'" + nome_usuario + "'"
        )
    ).json[0]["usuario_id"]

    datahora_atual = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    DATABASE.insert_all(
        "Resposta",
        [
            "'" + str(uuid.uuid4()) + "'",
            "'" + post_id + "'",
            "'" + descricao + "'",
            "'" + usuario + "'",
            "'" + str(datahora_atual) + "'",
        ],
    )
    return redirect("/")
