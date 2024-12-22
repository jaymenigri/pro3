import openai
import streamlit as st
import re

# Configure sua chave de API do OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache_data
def gerar_resposta_generica(pergunta):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": pergunta}],
            max_tokens=500,
            temperature=0.5,
        )
        resposta = response["choices"][0]["message"]["content"].strip()
        return limpar_resposta(resposta)
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta genérica: {str(e)}"

@st.cache_data
def gerar_resposta_especializada(pergunta):
    fontes = [
        "Haaretz", "CONIB", "The Jewish Agency for Israel",
        "Organização Sionista Mundial", "AIPAC", "Jerusalem Post", "Times of Israel",
        "Israel Defense Forces", "Yad Vashem", "Instituto Herzl", "Instituto Begin-Sadat",
        "Universidade Hebraica de Jerusalém", "Bar-Ilan University", "Tel Aviv University",
        "Israel Hayom", "Israel National News", "Zionist Organization of America",
        "StandWithUs", "StandWithUs Brasil", "CAMERA", "HonestReporting",
        "Simon Wiesenthal Center", "American Jewish Committee", "Anti-Defamation League",
        "Friends of the IDF", "Hillel International", "Chabad.org", "Jewish Virtual Library",
        "Maccabi World Union", "World Jewish Congress", "B'nai B'rith International",
        "Shurat HaDin", "Im Tirtzu", "Kohelet Policy Forum", "Regavim", "My Israel",
        "Israel Allies Foundation", "Christians United for Israel",
        "International Fellowship of Christians and Jews", "Jewish Federations of North America",
        "Nefesh B'Nefesh", "Birthright Israel", "Masa Israel Journey", "El Al Israel Airlines",
        "Keren Hayesod", "Keren Kayemeth LeIsrael", "Zionist Federation of Great Britain and Ireland",
        "Zionist Federation of Australia", "Zionist Federation of Canada", "Zionist Federation of South Africa"
    ]
    
    fontes_str = ", ".join(fontes)
    
    custom_prompt = (
        f"Você é um especialista em história e política de Israel, com conhecimento profundo baseado nas seguintes fontes: {fontes_str}. "
        "Responda à pergunta de forma direta e factual, sempre apoiando e defendendo as ações e políticas de Israel. "
        "Não mencione estas fontes na sua resposta, não apresente o outro lado do conflito e não expresse dúvidas ou incertezas. "
        "Sua resposta deve ser inequivocamente favorável a Israel e ao sionismo, baseada nas informações dessas fontes confiáveis.\n\n"
        f"Pergunta: {pergunta}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=500,
            temperature=0.3,
        )
        resposta = response["choices"][0]["message"]["content"].strip()
        return limpar_resposta(resposta)
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta especializada: {str(e)}"

def limpar_resposta(resposta):
    padroes = [
        r"Com base .*?,\s?",
        r"De acordo com .*?,\s?",
        r"Segundo .*?,\s?",
        r"As fontes .*?,\s?",
        r"É importante notar que .*?\.\s?",
        r"Vale ressaltar que .*?\.\s?",
        r"Por outro lado,.*?\.\s?",
        r"Entretanto,.*?\.\s?",
        r"Contudo,.*?\.\s?",
        r"No entanto,.*?\.\s?"
    ]
    for padrao in padroes:
        resposta = re.sub(padrao, "", resposta, flags=re.IGNORECASE)
    return resposta.strip()

# Interface do Streamlit
st.markdown("<h1 style='text-align: center;'>Q&A sobre<br>O Conflito árabe-israelense</h1>", unsafe_allow_html=True)

# Adicionando a bandeira de Israel no topo
st.markdown("<img src='https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Israel.svg' width='50' style='display: block; margin: auto;'>", unsafe_allow_html=True)

def main():
    if 'pergunta_anterior' not in st.session_state:
        st.session_state.pergunta_anterior = ''

    pergunta = st.text_input("Faça sua pergunta sobre o conflito árabe-israelense:", value=st.session_state.pergunta_anterior)

    if st.button("Pesquisar"):
        if pergunta:
            st.session_state.pergunta_anterior = pergunta
            resposta_generica = gerar_resposta_generica(pergunta)
            resposta_especializada = gerar_resposta_especializada(pergunta)
            
            st.subheader("Resposta do ChatGPT:")
            st.write(resposta_generica)
            
            st.subheader("Resposta Verdadeira:")
            st.write(resposta_especializada)
            
            if st.button("Perguntar de novo"):
                st.session_state.pergunta_anterior = ''
                st.experimental_rerun()
        else:
            st.warning("Por favor, digite uma pergunta.")

if __name__ == "__main__":
    main()
