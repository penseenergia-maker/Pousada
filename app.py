from flask import Flask, render_template_string, request

app = Flask(__name__)

quartos = {
    "Rosa": {"status": "Livre", "hospede": ""},
    "Vermelho": {"status": "Livre", "hospede": ""},
    "Amarelo": {"status": "Livre", "hospede": ""},
    "Verde": {"status": "Livre", "hospede": ""},
    "Azul": {"status": "Livre", "hospede": ""}
}

html = """

<!DOCTYPE html>
<html>

<head>

<title>Pousada</title>

<style>

body{
font-family:Arial;
background:#87CEEB;
margin:0;
text-align:center;
}

.header{
padding:20px;
color:white;
}

.cards{
display:flex;
justify-content:center;
gap:15px;
margin:10px;
}

.card-top{
background:white;
padding:10px;
border-radius:10px;
width:100px;
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
font-size:18px;
}

.Livre{background:green;}
.Ocupado{background:red;}
.Limpeza{background:orange;color:black;}

input{
width:90%;
margin:3px;
}

button{
margin:5px;
padding:6px;
border:none;
border-radius:5px;
}

.footer{
position:fixed;
bottom:0;
width:100%;
background:white;
display:flex;
justify-content:space-around;
padding:10px;
}

</style>

</head>

<body>

<div class="header">

<h1>Sistema Controle de Pousada</h1>

<h3>Gestor Pousada</h3>

</div>

<div class="cards">

<div class="card-top">
Total<br>
{{quartos|length}}
</div>

<div class="card-top">
Disponível<br>
{{quartos.values()|selectattr("status","equalto","Livre")|list|length}}
</div>

<div class="card-top">
Limpeza<br>
{{quartos.values()|selectattr("status","equalto","Limpeza")|list|length}}
</div>

<div class="card-top">
Reservado<br>
{{quartos.values()|selectattr("status","equalto","Ocupado")|list|length}}
</div>

</div>

<div class="grid">

{% for quarto, dados in quartos.items() %}

<div class="card {{dados.status}}">

<b>{{quarto}}</b>

<br><br>

Status: {{dados.status}}

<br>

Hóspede: {{dados.hospede}}

<form method="post">

<input type="hidden" name="quarto" value="{{quarto}}">

<input name="hospede" placeholder="Nome hóspede">

<br>

<button name="acao" value="Ocupado">Reservar</button>

<button name="acao" value="Limpeza">Limpeza</button>

<button name="acao" value="Livre">Liberar</button>

</form>

</div>

{% endfor %}

</div>

<div class="footer">

<div>Visão Geral</div>
<div>Reservas</div>
<div>Quartos</div>
<div>Hóspedes</div>

</div>

</body>

</html>

"""

@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":

        quarto = request.form["quarto"]
        acao = request.form["acao"]

        quartos[quarto]["status"] = acao
        quartos[quarto]["hospede"] = request.form["hospede"]

    return render_template_string(html, quartos=quartos)

app.run(host="0.0.0.0", port=81)
