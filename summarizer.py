import os
from openai import OpenAI, OpenAIError, RateLimitError
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def summarize_text(prompt: str) -> str:
    try:
        client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
        r = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": "You summarize PDF text professionally."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
        return r.choice[0].message.content.strip()
    except RateLimitError:
        return "⚠️ You’ve exceeded your OpenAI quota. Check your billing or upgrade your plan."
    except OpenAIError as e:
        st.error(f"OpenAI Error: {str(e)}")