from flask import Flask, request, render_template
from contextlib import closing
import sqlite3

app = Flask(__name__)

@app.route("/")
def menu():
    return render_template("menu.html", mensagem = "")

def row_to_dict(description, row):
    if row == None:
        return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d


def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

@app.route("/cliente/novo", methods = ["GET"])
def form_criar_cliente_api():
    return render_template("form_cliente.html", id_cliente = "novo", nome_cliente = "", login = "", senha = "", cep = "")

@app.route("/cliente/novo", methods = ["POST"])
def criar_cliente_api():
    nome_cliente = request.form["nome_cliente"]
    login = request.form["login"]
    senha = request.form["senha"]
    cep = request.form["cep"]
    id_cliente = criar_cliente(nome_cliente, login, senha, cep)
    return render_template("menu.html", mensagem = f"O Cliente {nome_cliente} foi Cadastrado!!")


sql_create = ''' CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente VARCHAR(50) NOT NULL,
    login VARCHAR(20) NOT NULL,
    senha VARCHAR(20) NOT NULL,
    cep VARCHAR(8) NOT NULL
);
'''

def conectar():
    return sqlite3.connect('rrg_games.db')

def criar_bd():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()

def criar_cliente(nome_cliente, login, senha, cpf):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO cliente (nome_cliente, login, senha, cep) VALUES (?, ?, ?, ?)", (nome_cliente, login, senha, cep))
        id_cliente = cur.lastrowid
        con.commit()
        return id_cliente        
   
if __name__ == "__main__":
    criar_bd()
    app.run(host='127.0.0.1', port=8000)