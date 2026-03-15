from flask import Flask, render_template_string, request

app = Flask(__name__)

quartos = {
    "Rosa": {"status": "Livre", "hospede": "", "entrada": "", "saida": ""},
    "Vermelho": {"status": "Livre", "hospede": "", "entrada": "", "saida": ""},
    "Amarelo": {"status": "Livre", "hospede": "", "entrada": "", "saida": ""},
    "Azul": {"status": "Livre", "hospede": "", "entrada": "", "saida": ""},
    "Verde": {"status": "Livre", "hospede": "", "entrada": "", "saida": ""},
    "Laranja": {"status": "Livre", "hospede": "", "entrada": "", "saida": ""}
}

html = """

<!DOCTYPE html>
<html>

<head>

<title>Pousada</title>

<style>

body{
font-family:Arial;
background:#f4f4f4;
text-align:center;
}

.grid{
display:grid;
grid-template-columns:repeat(3,1fr);
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

</style>

</head>

<body>

<h1>Controle da Pousada</h1>

<div class="grid">

{% for quarto, dados in quartos.items() %}

<div class="card {{dados.status}}">

<b>{{quarto}}</b>

<br>

Status: {{dados.status}}

<br><br>

Hóspede: {{dados.hospede}}

<br>

Entrada: {{dados.entrada}}

<br>

Saída: {{dados.saida}}

<form method="post">

<input type="hidden" name="quarto" value="{{quarto}}">

<input name="hospede" placeholder="Nome do hóspede">

<input name="entrada" placeholder="Data entrada">

<input name="saida" placeholder="Data saída">

<br>

<button name="acao" value="Ocupado">Check-in</button>

<button name="acao" value="Limpeza">Limpeza</button>

<button name="acao" value="Livre">Check-out</button>

</form>

</div>

{% endfor %}

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
        quartos[quarto]["entrada"] = request.form["entrada"]
        quartos[quarto]["saida"] = request.form["saida"]

    return render_template_string(html, quartos=quartos)

app.run(host="0.0.0.0", port=81)
