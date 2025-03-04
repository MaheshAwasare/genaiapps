import streamlit as st
import requests


# Function to call local LLM API and generate story
def generate_story(genre, num_characters, ending, setting, subject):
    OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
    system_prompt = ('Your goal is to create novel stories based on given genere and characters. You are an expert '
                     'story teller.')
    conversation_string = f"Create a story on {subject} of a  {genre} Genere with {num_characters} characters with their names from {setting} country."
    conversation_string += f"the story should have {ending} ending."

    print(f"Conversation String {conversation_string} ")

    OLLAMA_PROMPT = f"{system_prompt}: {conversation_string}"
    print(f"Prompt to model {OLLAMA_PROMPT}")
    OLLAMA_DATA = {
        "model": "phi",
        "prompt": OLLAMA_PROMPT,
        "stream": False,
        "keep_alive": "1m",
    }
    response = requests.post(OLLAMA_ENDPOINT, json=OLLAMA_DATA)
    summary = response.json()["response"]
    print(summary)
    return summary
    return story


# Streamlit UI
st.title("Personalized Storyteller")

# Genre selection
genre = st.selectbox("Select Story Genre:", ["Fantasy", "Comedy", "Mystery", "Adventure", "Romance"])

# Number of characters selection
num_characters = st.slider("Number of Characters:", min_value=1, max_value=7, value=2)

# Ending selection
ending = st.selectbox("Select Ending:", ["Happy", "Sad", "Comedy"])

subject = st.text_area("Input your story idea:")

# Setting selection
setting = st.selectbox("Select Setting:", ["Western", "Indian", "African", "Asian", "American"])
# Button to generate story
if st.button("Generate Story"):
    # Call function to generate story
    story = generate_story(genre, num_characters, ending, setting, subject)
    # Display generated story
    st.subheader("Your personalized story:")
    st.markdown(f"**Genre:** {genre}")
    st.markdown(f"**Number of Characters:** {num_characters}")
    st.markdown(f"**Ending:** {ending}")
    st.markdown(f"**Setting:** {setting}")
    st.write("")
    st.write(story)
