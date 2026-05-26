from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def calcular_emissoes(dados):
    """
    Calcula emissões de carbono e créditos ambientais
    """

    # =========================
    # DADOS RECEBIDOS
    # =========================

    distancia_km = float(dados.get("distancia_km", 0))
    tipo_transporte = dados.get("tipo_transporte", "carro")

    consumo_kwh = float(dados.get("consumo_kwh", 0))
    consumo_gas = float(dados.get("consumo_gas", 0))

    quantidade_residuos = float(dados.get("quantidade_residuos", 0))

    arvores_plantadas = int(dados.get("arvores_plantadas", 0))
    energia_renovavel = float(dados.get("energia_renovavel", 0))

    # =========================
    # FATORES DE EMISSÃO
    # =========================

    fatores_emissao_transporte = {
        "carro": 0.192,
        "moto": 0.071,
        "onibus": 0.105,
        "metro": 0.006,
        "bicicleta": 0,
        "a pe": 0,
        "carro_eletrico": 0.053
    }

    fator_emissao_energia = 0.0385
    fator_emissao_gas = 0.048
    fator_emissao_residuos = 0.57

    # =========================
    # CÁLCULO DAS EMISSÕES
    # =========================

    emissao_transporte = (
        distancia_km
        * 12
        * fatores_emissao_transporte.get(tipo_transporte, 0)
    )

    emissao_energia = consumo_kwh * 12 * fator_emissao_energia

    emissao_gas = consumo_gas * 12 * fator_emissao_gas

    emissao_residuos = (
        quantidade_residuos
        * 12
        * fator_emissao_residuos
    )

    emissao_total = (
        emissao_transporte
        + emissao_energia
        + emissao_gas
        + emissao_residuos
    )

    # =========================
    # CRÉDITOS DE CARBONO
    # =========================

    fator_sequestro_arvore = 22
    fator_energia_renovavel = 0.085

    credito_arvores = (
        arvores_plantadas
        * fator_sequestro_arvore
    )

    credito_energia_renovavel = (
        energia_renovavel
        * 12
        * fator_energia_renovavel
    )

    credito_total = (
        credito_arvores
        + credito_energia_renovavel
    )

    # =========================
    # EMISSÃO LÍQUIDA
    # =========================

    emissao_liquida = max(
        0,
        emissao_total - credito_total
    )

    # =========================
    # ÁRVORES NECESSÁRIAS
    # =========================

    arvores_necessarias = max(
        0,
        emissao_liquida / fator_sequestro_arvore
    )

    # =========================
    # CUSTO DE COMPENSAÇÃO
    # =========================

    preco_credito_por_tonelada = 20
    taxa_cambio = 5.00

    custo_compensacao_real = max(
        0,
        (emissao_liquida / 1000)
        * preco_credito_por_tonelada
        * taxa_cambio
    )

    # =========================
    # CLASSIFICAÇÃO
    # =========================

    if emissao_liquida < 2000:
        classificacao = "Baixa Pegada de Carbono"

    elif emissao_liquida < 5000:
        classificacao = "Pegada Moderada"

    else:
        classificacao = "Alta Pegada de Carbono"

    # =========================
    # DICAS
    # =========================

    dicas = [
        "Cada árvore pode sequestrar aproximadamente 22 kg de CO₂ por ano.",
        "Energia renovável reduz significativamente as emissões.",
    ]

    if emissao_transporte > 1000:
        dicas.append(
            "Considere utilizar transporte coletivo, bicicleta ou carro elétrico."
        )

    if emissao_energia > 1000:
        dicas.append(
        )

    if emissao_gas > 500:
        dicas.append(
            "Tente reduzir o consumo de gás utilizando equipamentos mais economicos."
        )

    if emissao_residuos > 500:
        dicas.append(
            "Separe resíduos recicláveis e reduza desperdícios."
        )

    # =========================
    # DADOS PARA GRÁFICOS
    # =========================

    grafico_emissoes = {
        "labels": [
            "Transporte",
            "Energia",
            "Gás",
            "Resíduos"
        ],
        "valores": [
            round(emissao_transporte, 2),
            round(emissao_energia, 2),
            round(emissao_gas, 2),
            round(emissao_residuos, 2)
        ]
    }

    grafico_creditos = {
        "labels": [
            "Árvores",
            "Energia Renovável"
        ],
        "valores": [
            round(credito_arvores, 2),
            round(credito_energia_renovavel, 2)
        ]
    }

    # =========================
    # RETORNO
    # =========================

    return {
        "emissao_total": round(emissao_total, 2),

        "credito_total": round(credito_total, 2),

        "emissao_liquida": round(emissao_liquida, 2),

        "arvores_necessarias": round(arvores_necessarias),

        "custo_compensacao_real": round(
            custo_compensacao_real,
            2
        ),

        "classificacao": classificacao,

        "dicas": dicas,

        "grafico_emissoes": grafico_emissoes,

        "grafico_creditos": grafico_creditos
    }


# =====================================
# ROTAS
# =====================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/como-funciona")
def como_funciona():
    return render_template("comofunciona.html")


@app.route("/calcular", methods=["POST"])
def calcular():

    dados = request.json

    resultado = calcular_emissoes(dados)

    return jsonify(resultado)


# =====================================
# EXECUÇÃO
# =====================================

if __name__ == "__main__":
    app.run(debug=True)