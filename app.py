from flask import Flask, render_template, request, jsonify
from rapidfuzz import process

app = Flask(__name__)

# Base de perguntas e respostas sobre o dia-a-dia
respostas = {
    "como está o tempo hoje?": "Para saber a previsão do tempo, acesse: https://tempo.inmet.gov.br ou consulte seu app de clima favorito.",
    "onde posso imprimir documentos?": "Você pode imprimir documentos em papelarias ou gráficas próximas.",
    "como faço para renovar um livro na biblioteca pública?": "A renovação pode ser feita pelo site da biblioteca ou presencialmente no balcão de atendimento.",
    "qual é o horário do ônibus para o centro?": "Os ônibus para o centro passam a cada 20 minutos, das 6h às 22h.",
    "onde encontro farmácias 24 horas?": "Você pode encontrar farmácias 24 horas pesquisando no Google Maps ou aplicativos de localização.",
    "qual o telefone do serviço de táxi?": "Taxi? Os taxis hoje estão muito caros! Indico você usar o aplicativo Uber ou 99",
    "como pedir comida por aplicativo?": "Baixe um app de delivery como iFood, Uber Eats ou 99Food, faça seu cadastro e escolha o restaurante.",
    "como reciclar lixo doméstico?": "Separe o lixo reciclável do orgânico e coloque nos coletores apropriados ou leve ao ponto de coleta mais próximo.",
    "qual supermercado está aberto agora?": "Consulte o horário de funcionamento dos supermercados no Google Maps ou no site do estabelecimento.",
    "como agendar consulta médica?": "Você pode agendar consultas pelo aplicativo do seu plano de saúde ou ligando para a clínica desejada.",
    "qual o número da emergência?": "O número de emergência é 190 para polícia, 192 para ambulância e 193 para bombeiros.",
    "como pedir um carro por aplicativo?": "Use apps como Uber ou 99, faça login, informe o destino e solicite o carro.",
    "onde tem caixa eletrônico perto de mim?": "Procure por caixas eletrônicos no Google Maps ou no app do seu banco.",
    "como faço para pagar uma conta online?": "Acesse o app do seu banco, escolha a opção de pagamentos e escaneie o código de barras da conta.",
    "onde posso comprar gás de cozinha?": "Você pode comprar gás de cozinha em depósitos especializados ou pedir por aplicativos de entrega."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    pergunta = request.json.get("mensagem", "").lower().strip()

    # Respostas para saudações
    saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "e aí", "oii", "oiii"]
    if any(s in pergunta for s in saudacoes):
        return jsonify({"resposta": "Olá! Como posso ajudar você hoje?"})

    # Encontra a pergunta mais parecida
    melhor_pergunta, score, _ = process.extractOne(pergunta, respostas.keys())
    
    if score > 60:  # nível de confiança (0 a 100)
        resposta = respostas[melhor_pergunta]
    else:
        resposta = "Desculpe, não entendi sua pergunta."
    
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
