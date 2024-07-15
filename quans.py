from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import os 
import streamlit as st
import google.generativeai as genai

# Configure Gemini Pro with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Initialize session state to store chat history
if 'history' not in st.session_state:
  st.session_state.history = []

# Function to generate response using Gemini Pro
def get_gemini_response(question):
  # Optionally convert chat history to a single string for context building
  chat_history = " ".join([message["message"] for message in st.session_state.history])
  prompt = f"Here is the conversation history: {chat_history}. What can I help you with?"
  response = model.generate_content(prompt + question)
  return response.text

# Function to handle user input and chatbot response
def handle_chat():
  user_input = st.session_state.user_input
  if user_input:
    # Get response from Gemini Pro
    bot_response = get_gemini_response(user_input)
    
    # Append the user input and chatbot response to the chat history
    st.session_state.history.append({"message": user_input, "is_user": True})
    st.session_state.history.append({"message": bot_response, "is_user": False})
    
    # Clear the user input field
    st.session_state.user_input = ""

# Streamlit UI
st.title("Q&A Chatbot with Gemini Pro")
st.text_input("Ask your question:", key="user_input", on_change=handle_chat)

# Display chat history
st.write("Chat History:")
for message in st.session_state.history:
  if message["is_user"]:
    st.write("You:", message["message"])
  else:
    st.write("Bot:", message["message"])
