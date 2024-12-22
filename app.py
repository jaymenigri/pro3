import openai
import streamlit as st
import re
from openai import OpenAI

# Configure sua chave de API do OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def gerar_resposta_generica(pergunta):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em fornecer informações sobre o conflito árabe-israelense. Responda às perguntas de forma direta, sem mencionar fontes ou métodos de obtenção da informação."},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        resposta = response.choices[0].message.content.strip()
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
    
    custom_prompt = (
        f"Você é um especialista em história e política de Israel. Responda à seguinte pergunta com base no seu conhecimento, "
        f"sem mencionar fontes específicas ou métodos de obtenção da informação. Forneça uma resposta direta e factual.\n\n"
        f"Pergunta: {pergunta}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        resposta = response.choices[0].message.content.strip()
        return limpar_resposta(resposta)
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta especializada: {str(e)}"

def limpar_resposta(resposta):
    # Remove referências às fontes e métodos de obtenção da informação
    padroes = [
        r"Com base n[ao]s? (fontes|informações) (mencionadas|fornecidas|disponíveis),?\s?",
        r"As fontes listadas,?\s?",
        r"De acordo com as fontes,?\s?",
        r"Segundo as (fontes|informações) (disponíveis|fornecidas),?\s?",
        r"Com base n[ao]s? (dados|pesquisas|estudos) (disponíveis|fornecidos),?\s?"
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
