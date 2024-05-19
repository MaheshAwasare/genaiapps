import streamlit as st
import requests

global_storyline = ""


# Function to call local LLM API and generate central storyline
def generate_central_storyline(genre, setting, story_locations, num_characters, ending):
    OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
    global global_storyline
    system_prompt = ('You are an expert '
                     'story teller.Your goal is to create novel storyline with given characters, genere and setting.'
                     'It should tell gist of story in crisp manner ')
    conversation_string = f"Create a storyline of a Genere {genre}  with {num_characters} characters from {setting} country. The story should have {story_locations} locations,the story should have {ending} ending."
    OLLAMA_PROMPT = f"{system_prompt}: {conversation_string}"
    OLLAMA_DATA = {
        "model": "phi",
        "prompt": OLLAMA_PROMPT,
        "stream": False,
        "keep_alive": "1m",
    }
    response = requests.post(OLLAMA_ENDPOINT, json=OLLAMA_DATA)
    global_storyline = response.json()["response"]
    print(global_storyline)
    return global_storyline


# Function to call local LLM API and generate introduction scenes
def generate_introduction_scenes(characters, intro_option, backstory, central_storyline):
    # Call your local LLM API here to generate introduction scenes based on inputs
    # Replace this with your actual code to generate the scenes
    global global_storyline
    introduction_scenes = "Introduction Scenes:\n"
    introduction_scenes += f"{central_storyline}\n"  # Incorporate central storyline into introduction scenes
    if intro_option == "Single Introduction Scene":
        introduction_scenes += "In a bustling city, we meet our main characters:\n"
        for character in characters:
            introduction_scenes += f"{character}: {backstory[character]}\n"
    else:  # Multiple Introduction Scenes
        for character in characters:
            introduction_scenes += f"{character}: {backstory[character]}\n"
            introduction_scenes += f"In a vibrant city, we are introduced to {character}.\n"
    return introduction_scenes


# Function to call local LLM API and generate other scenes
def generate_other_scenes(scene_inputs):
    # Call your local LLM API here to generate other scenes based on inputs
    # Replace this with your actual code to generate the scenes
    other_scenes = "Other Scenes:\n"
    for i, scene_input in enumerate(scene_inputs, start=1):
        other_scenes += f"Scene {i}: {scene_input}\n"
    return other_scenes


# Function to call local LLM API and generate ending
def generate_ending(ending_input):
    # Call your local LLM API here to generate the ending based on inputs
    # Replace this with your actual code to generate the ending
    ending = f"Ending: {ending_input}"
    return ending


def get_characters(storyline):
    OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
    global global_storyline
    system_prompt = ('Extract ONLY people names like John, Rohit from given storyline. Just give list of names, no other words in this answer. ')
    OLLAMA_PROMPT = f"{system_prompt}: {storyline}"
    OLLAMA_DATA = {
        "model": "phi",
        "prompt": OLLAMA_PROMPT,
        "stream": False,
        "keep_alive": "1m",
    }
    response = requests.post(OLLAMA_ENDPOINT, json=OLLAMA_DATA)
    characters = response.json()["response"]
    print(characters)
    return characters


# Streamlit UI
st.title("Hindi Movie Maker")

# Sidebar options
option = st.sidebar.selectbox("Select Option:", ["Generate Storyline", "Generate Introduction Scenes",
                                                 "Generate Other Scenes", "Generate Ending"])

if option == "Generate Storyline":
    st.header("Generate Central Storyline")
    # User inputs
    genre = st.selectbox("Select Genre:", ["Romance", "Action", "Comedy", "Drama"])
    setting = st.selectbox("Select Setting:", ["Western", "Indian", "African", "Asian", "American"])
    story_locations = st.multiselect("Select Story Locations:", ["India", "Abroad"])
    # Number of characters selection
    num_characters = st.slider("Number of Characters:", min_value=1, max_value=7, value=2)

    ending = st.selectbox("Select Ending:", ["Happy", "Sad", "Comedy"])
    # Button to generate central storyline
    if st.button("Generate"):
        # Call function to generate central storyline
        central_storyline = generate_central_storyline(genre, setting, story_locations, num_characters, ending)
        # Display generated central storyline
        st.subheader("Central Storyline:")
        st.write(central_storyline)

elif option == "Generate Introduction Scenes":
    st.header("Generate Introduction Scenes")
    # Retrieve central storyline from global variable
    central_storyline = global_storyline
    # Retrieve characters from central storyline
    characters = get_characters(central_storyline)
    print(f"Characters {characters}")
    if not characters:
        st.warning("Characters not found in the storyline.")
    else:
        # Parse central storyline to extract backstory
        # For demonstration, we'll use predefined backstories
        backstory = {}
        for character in characters:
            backstory[character] = st.text_input(f"{character} Backstory:")
        # User input for introduction option
        intro_option = st.radio("Choose Introduction Option:",
                                ["Single Introduction Scene", "Multiple Introduction Scenes"])
        # Button to generate introduction scenes
        if st.button("Generate"):
            # Call function to generate introduction scenes
            introduction_scenes = generate_introduction_scenes(characters, intro_option, backstory)
            # Display generated introduction scenes
            st.subheader("Introduction Scenes:")
            st.write(introduction_scenes)

elif option == "Generate Other Scenes":
    st.header("Generate Other Scenes")
    # Retrieve central storyline from previous step
    central_storyline = st.text_area("Central Storyline:", height=200)
    # User inputs for other scenes
    num_scenes = st.number_input("Enter the number of scenes:", min_value=1, value=5)
    scene_inputs = []
    for i in range(num_scenes):
        scene_inputs.append(st.text_input(f"Scene {i + 1} Input:"))
    # Button to generate other scenes
    if st.button("Generate"):
        # Call function to generate other scenes
        other_scenes = generate_other_scenes(scene_inputs)
        # Display generated other scenes
        st.subheader("Other Scenes:")
        st.write(other_scenes)

elif option == "Generate Ending":
    st.header("Generate Ending")
    # Retrieve central storyline from previous step
    central_storyline = st.text_area("Central Storyline:", height=200)
    # User input for ending
    ending_input = st.text_input("Enter the ending:")
    # Button to generate ending
    if st.button("Generate"):
        # Call function to generate ending
        ending = generate_ending(ending_input)
        # Display generated ending
        st.subheader("Ending:")
        st.write(ending)
