import os
import sqlite3

os.makedirs("templates", exist_ok=True)

app_py = '''
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "pousada"

usuarios = {
    "super": {"senha":"123","nivel":"super"},
    "admin": {"senha":"123","nivel":"admin"},
    "operador": {"senha":"123","nivel":"operador"}
}

def conectar():
    return sqlite3.connect("dados.db")


@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        u = request.form["usuario"]
        s = request.form["senha"]

        if u in usuarios and usuarios[u]["senha"] == s:

            session["usuario"] = u
            session["nivel"] = usuarios[u]["nivel"]

            return redirect("/painel")

    return render_template("login.html")


@app.route("/painel")
def painel():

    if "usuario" not in session:
        return redirect("/")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quartos")
    quartos = cursor.fetchall()

    conn.close()

    ver_valores = session["nivel"] in ["super","admin"]

    return render_template(
        "painel.html",
        quartos=quartos,
        ver_valores=ver_valores
    )


@app.route("/atualizar", methods=["POST"])
def atualizar():

    quarto = request.form["quarto"]
    status = request.form["status"]
    hospede = request.form["hospede"]
    entrada = request.form["entrada"]
    saida = request.form["saida"]
    valor = request.form.get("valor",0)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE quartos
    SET status=?, hospede=?, entrada=?, saida=?, valor=?
    WHERE nome=?
    """,(status,hospede,entrada,saida,valor,quarto))

    conn.commit()
    conn.close()

    return redirect("/painel")


app.run(host="0.0.0.0",port=81)
'''

login_html = '''
<h2>Login Sistema Controle de Pousada</h2>

<form method="post">

Usuário<br>
<input name="usuario"><br>

Senha<br>
<input type="password" name="senha"><br><br>

<button>Entrar</button>

</form>
'''

painel_html = '''
<!DOCTYPE html>
<html>

<head>

<style>

body{
font-family:Arial;
background:#87CEEB;
text-align:center;
}

.grid{
display:grid;
grid-template-columns:repeat(2,1fr);
gap:20px;
padding:20px;
}

.card{
padding:20px;
border-radius:10px;
color:white;
}

.Livre{background:green;}
.Ocupado{background:red;}
.Limpeza{background:orange;color:black;}

</style>

</head>

<body>

<h1>Sistema Controle de Pousada</h1>
<h3>Gestor Pousada</h3>

<div class="grid">

{% for q in quartos %}

<div class="card {{q[1]}}">

<b>{{q[0]}}</b>

<br>

Status: {{q[1]}}

<br>

Hóspede: {{q[2]}}

<br>

Entrada: {{q[3]}}

<br>

Saída: {{q[4]}}

{% if ver_valores %}

<br>

Valor: {{q[5]}}

{% endif %}

<form action="/atualizar" method="post">

<input type="hidden" name="quarto" value="{{q[0]}}">

<input name="hospede" placeholder="Hóspede">

<input name="entrada" type="date">

<input name="saida" type="date">

{% if ver_valores %}
<input name="valor" placeholder="Valor">
{% endif %}

<br>

<select name="status">
<option>Livre</option>
<option>Ocupado</option>
<option>Limpeza</option>
</select>

<br>

<button>Salvar</button>

</form>

</div>

{% endfor %}

</div>

</body>

</html>
'''

with open("app.py","w") as f:
    f.write(app_py)

with open("templates/login.html","w") as f:
    f.write(login_html)

with open("templates/painel.html","w") as f:
    f.write(painel_html)

conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quartos (
nome TEXT,
status TEXT,
hospede TEXT,
entrada TEXT,
saida TEXT,
valor REAL
)
""")

quartos = ["Rosa","Vermelho","Amarelo","Verde","Azul"]

for q in quartos:
    cursor.execute("INSERT INTO quartos VALUES (?,?,?,?,?,?)",(q,"Livre","","","",0))

conn.commit()
conn.close()

print("Sistema da pousada instalado com sucesso.")
