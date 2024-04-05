import streamlit as st
import os
#from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = "AIzaSyCnmP6DL8T-nquF-Okas_24TeiMzGHwrc4"
#load_dotenv()  # API key stored in .env file for security purpose
google_api_key = GOOGLE_API_KEY
st.header(":blue[Joke App  Using Generative AI]")  # App title
st.subheader(":orange[Powered by Google gemini-pro model]")
st.subheader("", divider='rainbow')
jokeType = st.sidebar.selectbox(
    "Select Joke types?",
    ("EveryDay Fun", "Office", "Programming", "Dark", "Pun", "Spooky")
)

noOfJokes = st.sidebar.selectbox(
    "Select number of jokes",
    (1, 2, 3)
)


def getJoke(noofjokes, joketype):
    prompt_string = f"Tell me COMPLETELY NEW (do not forget this) {noofjokes}  {joketype} jokes. Do not include scarecrow joke please"
    gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=google_api_key)
    result = gemini_llm.invoke(prompt_string)
    st.header(':blue[Generated Jokes]')
    st.write(result.content)


if st.sidebar.button("Generate Jokes"):
    getJoke(noOfJokes, jokeType)
