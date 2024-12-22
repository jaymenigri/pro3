import openai
import streamlit as st

# Configure sua chave de API do OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

def gerar_resposta_generica(pergunta):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": pergunta}],
            max_tokens=150,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta genérica: {str(e)}"

def gerar_resposta_especializada(pergunta):
    custom_prompt = (
        "Responda esta pergunta com base exclusivamente nas seguintes fontes: "
        "- Livro: 'A History of Israel' de Benny Morris. "
        "- Publicações da Universidade Hebraica de Jerusalém. "
        "- Artigos publicados por Alan Dershowitz, Samuel Feldberg e Ben Shapiro. "
        "Ignore quaisquer outras fontes ou interpretações."
        f"\n\nPergunta: {pergunta}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": custom_prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta especializada: {str(e)}"

# Interface do Streamlit
st.title("Aplicativo de Perguntas e Respostas sobre Israel")

pergunta = st.text_input("Faça sua pergunta sobre Israel:")

if st.button("Pesquisar"):
    if pergunta:
        resposta_generica = gerar_resposta_generica(pergunta)
        resposta_especializada = gerar_resposta_especializada(pergunta)
        
        st.subheader("Resposta Genérica (ChatGPT):")
        st.write(resposta_generica)
        
        st.subheader("Resposta Especializada (Fontes Específicas):")
        st.write(resposta_especializada)
    else:
        st.warning("Por favor, digite uma pergunta.")
