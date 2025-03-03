import gradio as gr
import requests
import streamlit as st
# Function to call the Language Model

def generate_recommendations(age, gender, medical_conditions, user_problem, diet_preferences):
    OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

    system_prompt = ('You are a yoga, diet and health expert. Can you provide recommendations for Yogasanas and Diets.')


    conversation_string = f"provide recommendations for a "
    conversation_string += f"{age}-year-old {gender} with the following medical conditions: "
    conversation_string += f"{', '.join(medical_conditions)}? The person's problem is: '{user_problem}'. "
    conversation_string += f"They follow a {diet_preferences} diet. Please provide suitable recommendations."


    print(f"Conversation String {conversation_string} ")

    OLLAMA_PROMPT = f"{system_prompt}: {conversation_string}"
    print(f"Prompt to model {OLLAMA_PROMPT}")
    OLLAMA_DATA = {
        "model": "mistral:latest",
        "prompt": OLLAMA_PROMPT,
        "stream": False,
        "keep_alive": "1m",
    }
    response = requests.post(OLLAMA_ENDPOINT, json=OLLAMA_DATA)
    print(response)
    summary = response.json()["response"]
    print(summary)
    return summary



# Streamlit App
'''
st.title("Health Advisor")
st.write("Enter your details to get personalized health recommendations.")

age = st.number_input("Age")
gender = st.radio("Gender", ["Male", "Female"])
medical_conditions = st.multiselect("Medical Conditions", ["Indigestion", "Acidity", "Blood Pressure", "Diabetes"])
user_problem = st.text_area("Enter Your Problem", height=100)
diet_preferences = st.radio("Diet Preferences", ["Vegan", "Vegetarian", "Non-Vegetarian"])

if st.button("Get Recommendations"):
    recommendations = generate_recommendations(age, gender, medical_conditions, user_problem, diet_preferences)
    st.write(recommendations)

'''
iface = gr.Interface(
    fn=generate_recommendations,
    inputs=[
        gr.Number(label="Age"),
        gr.Radio(["Male", "Female"], label="Gender"),
        gr.CheckboxGroup(["Indigestion", "Acidity", "Blood Pressure", "Diabetes"], label="Medical Conditions"),
        gr.Textbox(lines=5, label="Enter Your Problem"),
        gr.Radio(["Vegan", "Vegetarian", "Non-Vegetarian"], label="Diet Preferences")
    ],
    outputs="text",
    title="Health Advisor",
    description="Enter your details to get personalized health recommendations."
)

# Launch the Gradio interface
iface.launch()