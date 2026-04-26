import streamlit as st
import time

def add_questions_ui(save_questions_callback) :
    st.subheader("Add New Questions")

    if "form_data" not in st.session_state :
        st.session_state["form_data"] = {
            "question" : "",
            "option_a" : "", 
            "option_b" : "", 
            "option_c" : "", 
            "option_d" : "", 
            "correct_answer" : "A",
            "explanation" : "",
        }
    if "message" not in st.session_state :
        st.session_state["message"] = ""
    st.session_state.form_data["question"] = st.text_area("Question", value = st.session_state.form_data["question"], placeholder = "Enter the question here...")
    st.session_state.form_data["option_a"] = st.text_area("Option A", value = st.session_state.form_data["option_a"], placeholder = "Enter option A...")
    st.session_state.form_data["option_b"] = st.text_area("Option B", value = st.session_state.form_data["option_b"], placeholder = "Enter option B...")
    st.session_state.form_data["option_c"] = st.text_area("Option C", value = st.session_state.form_data["option_c"], placeholder = "Enter option C...")
    st.session_state.form_data["option_d"] = st.text_area("Option D", value = st.session_state.form_data["option_d"], placeholder = "Enter option D...")
    st.session_state.form_data["answer"] = st.selectbox("Correct Answer", ["A", "B", "C", "D"], index = ["A", "B", "C", "D"].index(st.session_state.form_data["correct_answer"]))
    st.session_state.form_data["explanation"] = st.text_area("Explanation (optional)", value = st.session_state.form_data["explanation"], placeholder = "Enter explanation...")

    col1, col2 = st.columns(2)

    if st.session_state["message"] :
        st.info(st.session_state["message"])
    with col1 :
        if st.button("Save Question") :
            if "questions" not in st.session_state :
                st.session_state.questions = []
            existing_questions = [q["question"] for q in st.session_state.questions]
            if st.session_state.form_data["question"].strip() in existing_questions :
                st.session_state["message"] = "This question already exists. Please enter a new unique question."
            elif not st.session_state.form_data["question"].strip() or not st.session_state.form_data["option_a"].strip() or not st.session_state.form_data["option_b"].strip() :
                st.session_state["message"] = "Question and at least TWO options are required."
            else : 
                new_question = {
                    "question" : st.session_state.form_data["question"].strip(),
                    "options" : {
                        "A" : st.session_state.form_data["option_a"].strip(),
                        "B" : st.session_state.form_data["option_b"].strip(),
                        "C" : st.session_state.form_data["option_c"].strip(), 
                        "D" : st.session_state.form_data["option_d"].strip(),
                    },
                    "correct_answer" : st.session_state.form_data["correct_answer"],
                    "exlpanation" : st.session_state.form_data["explanation"].strip() if st.session_state.form_data["explanation"] else None,
                }
                st.session_state.questions.append(new_question)
                save_questions_callback(st.session_state.questions)
                st.session_state["message"] = "Question successfully added!"

    with col2 :
        if st.button("Clear Form") :
            st.session_state.form_data = {
                "question" : "",
                "option_a" : "",
                "option_b" : "", 
                "option_c" : "",
                "option_d" : "", 
                "correct_answer" : "A",
                "explanation" : "",
            }
            st.session_state["message"] = "Form successfully cleared!"

            time.sleep(1)
            st.session_state["message"] = ""