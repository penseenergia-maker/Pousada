from flask import Flask, render_template_string, request

app = Flask(__name__)

quartos = {
    "Rosa": "Livre",
    "Vermelho": "Livre",
    "Amarelo": "Livre",
    "Azul": "Livre",
    "Verde": "Livre"
}

html = """
<h1>Controle da Pousada</h1>

{% for quarto, status in quartos.items() %}
<p>
<b>{{quarto}}</b> - {{status}}
<form method="post">
<input type="hidden" name="quarto" value="{{quarto}}">
<button name="acao" value="Ocupado">Ocupar</button>
<button name="acao" value="Livre">Liberar</button>
</form>
</p>
{% endfor %}
"""

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        quartos[request.form["quarto"]] = request.form["acao"]
    return render_template_string(html, quartos=quartos)

app.run(host="0.0.0.0", port=3000)
