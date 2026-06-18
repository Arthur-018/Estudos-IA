import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="Assistente de Chat", page_icon="🤖", layout="centered")
st.title("🤖 Meu Assistente de IA")
st.write("Interface integrada ao arquivo FRONT.md")

client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def ler_historico():
    if os.path.exists("./FRONT.md"):
        with open("./FRONT.md", "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    return "Nenhum histórico registrado ainda."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Pergunte-me qualquer coisa ou peça para eu consultar nosso histórico."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if resposta := st.chat_input("Digite sua pergunta..."):
    
    historico_conteudo = ler_historico()

    st.session_state.messages.append({"role": "user", "content": resposta})
    with st.chat_message("user"):
        st.markdown(resposta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                resposta_do_llm = client_openai.chat.completions.create(
                    model="google/gemma-4-12b-qat",
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                f"Você é o Assistente do Chat e seu objetivo é responder sobre tudo em geral. E você tem que ajudar o usuário com base no histórico fornecido.\n"
                                f"Você tem acesso total aos registros das conversations anteriores através do bloco abaixo:\n\n"
                                f"HISTÓRICO ATUAL DO CHAT:\n{historico_conteudo}\n\n"
                                f"DIRETRIZES:\n"
                                f"- Quando o usuário perguntar sobre o histórico, comandos passados ou qual foi a pergunta anterior, leia atentamente os dados acima para responder exatamente o que ele quer saber.\n"
                                f"- Seja direto e preciso ao resgatar as informações do histórico."
                            )
                        },
                        {"role": "user", "content": resposta}
                    ],
                    temperature=1.0,
                    max_tokens=1350
                )
                texto_resposta = resposta_do_llm.choices[0].message.content.strip()
            except Exception as e:
                texto_resposta = f"Erro ao conectar ao LM Studio: {e}. Garanta que o servidor local está ligado."

            st.markdown(texto_resposta)
            
    st.session_state.messages.append({"role": "assistant", "content": texto_resposta})

    with open("./FRONT.md", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Usuário: {resposta}\nIA: {texto_resposta}\n---\n")
