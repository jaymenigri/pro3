from openai import OpenAI
import streamlit as st
import re
import smtplib
from email.mime.text import MIMEText

# Inicialize o cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def gerar_resposta_generica(pergunta):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": pergunta}],
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
    
    fontes_str = ", ".join(fontes)
    
    custom_prompt = (
        f"Você é um especialista em história e política de Israel, com conhecimento profundo baseado nas seguintes fontes: {fontes_str}. "
        "Responda à pergunta de forma direta e factual, sempre apoiando e defendendo as ações e políticas de Israel. "
        "Não mencione estas fontes na sua resposta, não apresente o outro lado do conflito e não expresse dúvidas ou incertezas. "
        "Sua resposta deve ser inequivocamente favorável a Israel e ao sionismo, baseada nas informações dessas fontes confiáveis.\n\n"
        f"Pergunta: {pergunta}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=500,
            temperature=0.3,
        )
        resposta = response.choices[0].message.content.strip()
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

def enviar_email(feedback):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "jaymenigri@gmail.com"  # Substitua pelo seu email
    password = st.secrets["EMAIL_PASSWORD"]

    msg = MIMEText(feedback)
    msg['Subject'] = "Novo feedback do app Q&A sobre Conflito árabe-israelense"
    msg['From'] = sender_email
    msg['To'] = sender_email

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erro ao enviar email: {e}")
        return False
    finally:
        server.quit()

# Adicionando a bandeira de Israel no topo
st.markdown("<img src='https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Israel.svg' width='50' style='display: block; margin: auto;'>", unsafe_allow_html=True)

# Interface do Streamlit
st.markdown("<h1 style='text-align: center;'>Q&A sobre<br>o conflito árabe-israelense</h1><h2 style='text-align: center;'>@jaymenigri</h2>", unsafe_allow_html=True)

def main():
    if 'clear_input' not in st.session_state:
        st.session_state.clear_input = False

    pergunta = st.text_input("Faça sua pergunta sobre o conflito árabe-israelense:", value="" if st.session_state.clear_input else st.session_state.get('pergunta', ''))
    if st.session_state.clear_input:
        st.session_state.clear_input = False

    if st.button("Pesquisar"):
        if pergunta:
            st.session_state.pergunta = pergunta
            resposta_generica = gerar_resposta_generica(pergunta)
            resposta_especializada = gerar_resposta_especializada(pergunta)
            
            st.subheader("Resposta do ChatGPT:")
            st.write(resposta_generica)
            
            st.subheader("Resposta Verdadeira:")
            st.write(resposta_especializada)
            
            if st.button("Perguntar de novo"):
                st.session_state.clear_input = True
                st.experimental_rerun()
        else:
            st.warning("Por favor, digite uma pergunta.")

    # Seção de feedback
    st.markdown("---")
    st.subheader("Dê feedback e sugestões")
    feedback = st.text_area("Seu feedback:", height=100)
    if st.button("Enviar Feedback"):
        if feedback:
            if enviar_email(feedback):
                st.success("Feedback enviado com sucesso! Obrigado pela sua contribuição.")
            else:
                st.error("Houve um problema ao enviar o feedback. Por favor, tente novamente mais tarde.")
        else:
            st.warning("Por favor, escreva seu feedback antes de enviar.")

if __name__ == "__main__":
    main()
