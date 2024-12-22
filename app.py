import streamlit as st
import requests

def get_generic_response(question):
    # Simula uma resposta genérica
    return f"Resposta genérica para: {question}"

def get_specialized_response(question):
    # Simula uma resposta especializada
    return f"Resposta especializada sobre Israel para: {question}"

st.title("Perguntas sobre Israel")

question = st.text_input("Digite sua pergunta sobre Israel:")

if st.button("Pesquisar"):
    if question:
        generic_response = get_generic_response(question)
        specialized_response = get_specialized_response(question)
        
        st.subheader("Resposta Genérica:")
        st.write(generic_response)
        
        st.subheader("Resposta Especializada:")
        st.write(specialized_response)
    else:
        st.warning("Por favor, digite uma pergunta.")
