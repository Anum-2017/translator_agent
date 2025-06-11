import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

@cl.on_chat_start
async def welcome():
    await cl.Message(
        content="**Welcome to the Language Translator Agent By Anum Kamal!** 🌐\n\n"
                "Please use the format:\n"
                "`Translate: <sentence> | From: <source_language> | To: <target_language>`"
    ).send()

@cl.on_message
async def handle(message: cl.Message):
    try:
        content = message.content


        if "|" in content:
            parts = [p.strip() for p in content.split("|")]

            text = parts[0].replace("Translate:", "").strip()
            source = parts[1].replace("From:", "").strip()
            target = parts[2].replace("To:", "").strip()
            prompt = f"Translate this sentence from {source} to {target}:\n\n{text}"
        else:
            prompt = content

        
        response = model.generate_content(prompt)
        translated = response.text.strip()

        await cl.Message(content=translated).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
