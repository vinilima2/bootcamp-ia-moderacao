import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analisar_comentario(comentario):
    pergunta = (
        "Você é um moderador. Diga apenas 'ofensivo' ou 'não ofensivo' para o comentário:\n"
        f"{comentario}"
    )

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um moderador de conteúdo."},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=5,
            temperature=0
        )

        texto_resposta = resposta.choices[0].message["content"].strip().lower()
        aprovado = (texto_resposta == "não ofensivo")

        return {
            "aprovado": aprovado,
            "motivo": texto_resposta
        }

    except Exception as erro:
        return {
            "aprovado": False,
            "motivo": f"Erro ao usar a IA: {str(erro)}"
        }
