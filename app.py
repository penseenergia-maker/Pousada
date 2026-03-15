from flask import Flask, render_template_string, request

app = Flask(__name__)

# Lista de quartos
quartos = {
    "Rosa": "Livre",
    "Vermelho": "Livre",
    "Amarelo": "Livre",
    "Azul": "Livre",
    "Verde": "Livre",
    "Laranja": "Livre"
}

html = """
<!DOCTYPE html>
<html>
<head>
<title>Pousada</title>

<style>
body{
font-family: Arial;
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
font-size:20px;
}

.Livre{background:#2ecc71;}
.Ocupado{background:#e74c3c;}
.Limpeza{background:#f1c40f;color:black;}

button{
margin:5px;
padding:8px 12px;
border:none;
border-radius:6px;
cursor:pointer;
}
</style>

</head>

<body>

<h1>Controle da Pousada</h1>

<div class="grid">

{% for quarto, status in quartos.items() %}

<div class="card {{status}}">
<b>{{quarto}}</b><br><br>

Status: {{status}}

<form method="post">
<input type="hidden" name="quarto" value="{{quarto}}">

<br><br>

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
        quartos[quarto] = acao

    return render_template_string(html, quartos=quartos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
