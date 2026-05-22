import { inicializaModelo } from './modelo.js';
import { readFileSync } from "fs";

const model = await inicializaModelo("gemini-pro-vision");

function fileToGenerativePart(path, mimeType) {
  return {
    inlineData: {
      data: Buffer.from(readFileSync(path)).toString("base64"),
      mimeType
    },
  };
}

export async function processaImagem(imagem) {
  const prompt = "Me fale tudo que puder sobre o destino mostrado nessa imagem";

  const imageParts = [
    fileToGenerativePart(imagem, "image/jpeg"),
  ];

  const result = await model.generateContent([prompt, ...imageParts]);
  const response = await result.response;
  const text = response.text();
  console.log(text);

}