from openai import OpenAI
import os

client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

while True:
    resposta = input("Digite sua pergunta: ")
    if resposta == "":
        print("Sua pergunta não pode estar vazia.")
        continue
    elif resposta.lower() == "fim":
        print("IA encerrada!")
        break

    historico_conteudo = ""
    if os.path.exists("./README.MD"):
        with open("./README.MD", "r", encoding="utf-8") as arquivo:
            historico_conteudo = arquivo.read()
    else:
        historico_conteudo = "Nenhum histórico registrado ainda."

    resposta_do_llm = client_openai.chat.completions.create(
        model="google/gemma-4-e4b",
        messages=[
            {
                "role": "system", 
                "content": (
                    f"Você é o Assistente do Chat e seu objetivo é responder sobre tudo em geral. E você tem que me com o ajudar o usuário com base no histórico fornecido.\n"
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
    
    print("\n" + texto_resposta + "\n")

    with open("./README.MD", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Usuário: {resposta}\nIA: {texto_resposta}\n---\n")