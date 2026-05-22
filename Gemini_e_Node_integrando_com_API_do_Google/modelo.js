import { GoogleGenerativeAI } from '@google/generative-ai';

export async function inicializaModelo(modelo) {
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
  const model = genAI.getGenerativeModel({ model: modelo});
  return model;
}