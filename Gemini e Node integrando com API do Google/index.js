import { GoogleGenAI } from "@google/genai";
import { fazerPergunta } from "./pergunta.js";


const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY,
});

async function main() {
    try {
        let prompt = "Voce é um site de viagens e deve responder somente sobre esse assunto" +
        " Caso o usuário pergunte sobre algo diferente. Diga que não pode responder." +
        " O usuário escolheu: ";
        prompt += await fazerPergunta("Escreva qual lugar quer conhecer: ")
        
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: prompt,
        });

        console.log(response.text);
        
    } catch (error) {
        console.log("Erro ao chamar a IA.");
        
        if (error.status === 503) {
            console.log("O modelo está com alta demanda. tente novamente daqui a pouco.");
        } else {
            console.log(error.mensage);
            
        }
    }
}

main();