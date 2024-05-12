import requests
from langchain_community.llms import Ollama
llm = Ollama(model="phi")
import streamlit as st


def summarize_text(input_text):
    OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
    system_prompt = 'Your goal is to summarize the text given to you.Focus on providing a summary in freeform text.'
    conversation_string = input_text

    OLLAMA_PROMPT = f"{system_prompt}: {conversation_string}"
    OLLAMA_DATA = {
        "model": "phi",
        "prompt": OLLAMA_PROMPT,
        "stream": False,
        "keep_alive": "1m",
    }
    response = requests.post(OLLAMA_ENDPOINT, json=OLLAMA_DATA)
    summary=response.json()["response"]
    print(summary)
    return summary

def main():
    st.title("Text Summarization with Local LLM Model")
    user_input = st.text_area("Enter your long text here:")
    if st.button("Summarize"):
        if user_input:
            summary = summarize_text(user_input)
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter some text to summarize.")

if __name__=="__main__":
    main()


