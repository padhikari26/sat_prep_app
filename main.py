import streamlit as st
import requests
import os 
import json
from dotenv import load_dotenv
from add_questions import add_questions_ui
from view_questions import view_questions_ui
from practice import practice_page

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

QUESTIONS_FILE = "exam_questions.json"


def load_questions() :
    try :
        with open(QUESTIONS_FILE, "r") as file :
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) :
        return []


def save_questions(questions) :
    with open(QUESTIONS_FILE, "w") as file :
        json.dump(questions, file, indent = 4)


def get_conversational_response(chat_history) :
    headers = {
        "Authorization" : f"Bearer {API_KEY}",
        "Content-Type" : "application/json",
    }

    payload = {
        "model" : "llama-3.3-70b-versatile",
        "messages" : chat_history,
    }

    try :
        response = requests.post(API_URL, headers = headers, json = payload)
        if response.status_code == 200 :
            data = response.json()
            bot_reply = data.get("choices", [{}]).get("message", {}).get("content", "No response found.")
            return bot_reply
        else :
            return f"Error : Unable to get a response form the API. Status code : {response.status_code}\nDetails : {response.text}"
    except Exception as e :
        return f"An error occurred : {e}"


def save_questions_callback(questions) :
    st.session_stats["questions"] = questions
    try :
        file_path = "exam_questions.json"
        with open(file_path, "w") as f :
            json.dump(questions, f, indent = 4)
        st.success("Questions saved successfully to exam_questions.json!")
    except Exception as e :
        st.error(f"Error saving questions : {e}")

#streamlit app
def main() :
    st.title("Conversational SAT Prep Chatbot")
    st.sidebar.title("Navigation")
    options = st.sidebar.radio(
        "Choose an option: ",
        ["Home", "Add Questions", "View Questions", "Practice", "Chatbot"]
    )

    if options == "Home" :
        st.subheader("SAT Preparation Platfrom")
        st.write("Coming Soon !")

    elif options == "Add Questions" :
        add_questions_ui(save_questions_callback)
    
    elif options == "View Questions" :
        view_questions_ui()
    
    elif options == "Practice" :
        practice_page()
    
    elif options == "Chatbot" :
        st.subheader("SAT Prep Chatbot")
        st.write("Chat with the SAT Tutor to ask any questions you have about preparation, strategies, or practice.")

        if "chat_history" not in st.session_state :
            st.session_state.chat_history = [{"role" : "system", "content" : "You are a helpful SAT tutor."}]
        for msg in st.session_state.chat_history :
            if msg["role"] == "user" :
                st.markdown(f"**You: ** {msg["content"]}")
            elif msg["role"] == "assistant" :
                st.markdown(f"**SAT Tutor: ** {msg["content"]}")
        
        user_input = st.text_input("Your Message : ", placeholder = "Ask a question...")

        if st.button("Send") :
            if user_input.strip() :
                st.session_state.chat_history.append({"role" : "user", "content" : user_input.strip()})
                with st.spinner("SAT Tutor is thinking...") :
                    bot_reply = get_conversational_response(st.session_state.chat_history)
                st.session_state.chat_history.append({"role" : "assistant", "content" : bot_reply})

            else :
                st.warning("Please enter a message.")

if __name__ == "__main__" :
    main()