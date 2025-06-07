from flask import Flask, render_template, request, jsonify
from ia import analisar_comentario

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    # Corpo da requisição = {id_msg:str, msg:str, id_usuario:str} 
    data = request.get_json()
    msg = data.get('msg', '')
    # Chama a função de moderação do ia.py
    result = analisar_comentario(msg)
    return jsonify(result) 

if __name__ == "__main__": 
    app.run(debug=True)
