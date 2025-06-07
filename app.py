from flask import Flask, request, jsonify, render_template
from ia import analisar_comentario

# Configuração básica da aplicação Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    # Renderiza a página de chat
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    dados = request.get_json()
    comentario = dados.get('msg', '')
    # Chama a função de moderação do ia.py
    resultado = analisar_comentario(comentario)
    return jsonify(resultado)

if __name__ == '__main__':
    # Executa a aplicação em modo de desenvolvimento
    app.run(debug=True)
