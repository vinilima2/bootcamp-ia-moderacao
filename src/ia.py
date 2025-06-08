import openai

# Chave da API inserida diretamente
openai.api_key = "CHAVE" 

def analisar_comentario(comentario):
    # Prepara o prompt para a IA
    pergunta = (
        "Você é um moderador. Diga apenas 'ofensivo' ou 'não ofensivo' para o comentário:\n"
        f"{comentario}"
    ) 

    try:
        # Uso da interface openai-python >=1.0.0
        resposta = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um moderador de conteúdo."},
                {"role": "user",   "content": pergunta}
            ],
            max_tokens=5,
            temperature=0
        )

        # Extrai a resposta
        texto_resposta = resposta.choices[0].message.content.strip().lower()

        return {
            "aprovado": texto_resposta == "não ofensivo" or texto_resposta == "não ofensivo.",
            "motivo": texto_resposta
        }

    except Exception as erro:
        # Retorna mensagem de erro para debug
        return {
            "aprovado": False,
            "motivo": f"Erro ao usar a IA: {erro}"
        }
