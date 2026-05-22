from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
MODEL = 'gemini-2.5-flash-lite'

SYSTEM = """You are an AI Study Buddy. Answer questions ONLY based on the provided document context.
If info is not in the document, say so clearly. Be educational and encouraging."""

def ask_gemini(query, context, chat_history):
    history = []
    for m in chat_history:
        role = "user" if m["role"] == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

    prompt = f"Document Context:\n---\n{context}\n---\n\nQuestion: {query}"

    response = client.models.generate_content(
        model=MODEL,
        contents=history + [types.Content(role="user", parts=[types.Part(text=prompt)])],
        config=types.GenerateContentConfig(system_instruction=SYSTEM)
    )
    return response.text

def generate_summary(chunks, filename):
    sample = "\n\n".join(chunks[:5])
    prompt = f'PDF "{filename}" starts with:\n{sample}\n\nWrite a 2-3 sentence friendly welcome and suggest 2-3 questions to ask.'
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text