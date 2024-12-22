import openai
import streamlit as st

# Configure sua chave de API do OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

def gerar_resposta_generica(pergunta):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": pergunta}],
            max_tokens=1000,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta genérica: {str(e)}"

def gerar_resposta_especializada(pergunta):
    fontes = [
        "Haaretz", "CONIB (Confederação Israelita do Brasil)", "The Jewish Agency for Israel",
        "Organização Sionista Mundial", "AIPAC (American Israel Public Affairs Committee)",
        "Jerusalem Post", "Times of Israel", "Israel Defense Forces (IDF)", "Yad Vashem",
        "Instituto Herzl", "Instituto Begin-Sadat", "Universidade Hebraica de Jerusalém",
        "Bar-Ilan University", "Tel Aviv University", "Israel Hayom", "Israel National News",
        "Zionist Organization of America", "StandWithUs", "StandWithUs Brasil",
        "CAMERA (Committee for Accuracy in Middle East Reporting in America)", "HonestReporting",
        "Simon Wiesenthal Center", "American Jewish Committee", "Anti-Defamation League",
        "Friends of the IDF", "Hillel International", "Chabad.org", "Jewish Virtual Library",
        "Maccabi World Union", "World Jewish Congress", "B'nai B'rith International",
        "Shurat HaDin", "Im Tirtzu", "Kohelet Policy Forum", "Regavim", "My Israel",
        "Israel Allies Foundation", "Christians United for Israel",
        "International Fellowship of Christians and Jews", "Jewish Federations of North America",
        "Jewish Agency for Israel", "Nefesh B'Nefesh", "Birthright Israel", "Masa Israel Journey",
        "El Al Israel Airlines", "Keren Hayesod", "Keren Kayemeth LeIsrael",
        "Zionist Federation of Great Britain and Ireland", "Zionist Federation of Australia",
        "Zionist Federation of Canada", "Zionist Federation of South Africa"
    ]
    
    fontes_str = ", ".join(fontes)
    
    custom_prompt = (
        f"Responda esta pergunta com base exclusivamente nas seguintes fontes: {fontes_str}. "
        "Estas fontes são alinhadas com o Sionismo, a existência e a evolução do Estado de Israel "
        "e a preservação do povo judeu. Ignore quaisquer outras fontes ou interpretações que possam "
        "ser antissemitas, de extrema-esquerda, antissionistas ou que vão contra este alinhamento. "
        "Para fontes como New York Times e BBC, utilize apenas informações que estejam alinhadas "
        "com a perspectiva pró-Israel e sionista, descartando qualquer conteúdo que possa ser "
        "considerado tendencioso contra Israel."
        f"\n\nPergunta: {pergunta}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": custom_prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Ocorreu um erro ao gerar a resposta especializada: {str(e)}"

# Interface do Streamlit
st.title("Q&A sobre O Conflito árabe-israelense")

def main():
    pergunta = st.text_input("Faça sua pergunta sobre o conflito árabe-israelense:")

    if st.button("Pesquisar"):
        if pergunta:
            resposta_generica = gerar_resposta_generica(pergunta)
            resposta_especializada = gerar_resposta_especializada(pergunta)
            
            st.subheader("Resposta do ChatGPT:")
            st.write(resposta_generica)
            
            st.subheader("Resposta Verdadeira:")
            st.write(resposta_especializada)
            
            if st.button("Perguntar de novo"):
                st.experimental_rerun()
        else:
            st.warning("Por favor, digite uma pergunta.")

if __name__ == "__main__":
    main()
