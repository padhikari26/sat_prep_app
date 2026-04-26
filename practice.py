import streamlit as st

def practice_page() :
    questions = st.session_state.get("questions", [])

    if not questions :
        st.write("No questions available. Go to 'Add Questions' to add new ones.")
        return

    if "current_question_idx" not in st.session_state :
        st.session_state["current_question_idx"] = 0
    if "user_answers" not in st.session_state :
        st.session_state["user_answers"] = {}
    
    if "answered" not in st.session_state :
        st.session_state["answered"] = {}
    
    current_question_idx = st.session_state["current_question_idx"]

    question = questions[current_question_idx]
    st.subheader(f"Question {current_question_idx + 1}")
    st.write(question["question"])

    selected_answer = st.session_state["user_answers"].get(current_question_idx, "")
    if isinstance(question["options"], dict) :
        option_keys = list(question["options"].keys())
        selected_answer = st.radio("Choose an answer", option_keys, index = option_keys.index(selected_answer) if selected_answer in option_keys else 0)
    elif isinstance(question["options"], list) :
        selected_answer = st.radio("Choose an answer", question["options"], index = question["options"].index(selected_answer) if selected_answer in question["options"] else 0)
    
    st.session_state["user_answer"][current_question_idx] = selected_answer

    submit_answer = st.button("Submit Answer", key = f"sumbit_answer_{current_question_idx}")

    if submit_answer :
        correct_answer = question.get("answer")
        is_correct = selected_answer == correct_answer
        st.session_state["answered"][current_question_idx] = is_correct

        st.write(f"Your answer : {selected_answer}")
        st.write(f"Correct Asnwer : {correct_answer}")
        st.write(f"Your answer is {'correct' if is_correct else 'incorrect'}!")

    col1, col2, col3, col4 = st.colums([1, 1, 1, 1])

    with col1 :
        if st.button("First") and current_question_idx != 0 :
            st.session_state["current_question_idx"] = 0
            st.session_state["answered"][current_question_idx] = False
    
    with col2 :
        if st.button("Prev") and current_question_idx > 0 and current_question_idx != 0 :
            st.session_state["current_question_idx"] = current_question_idx - 1
            st.session_state["answered"][current_question_idx] = False
    
    with col3 :
        if st.button("Next") and current_question_idx < len(question) - 1 and current_question_idx in st.session_state["answered"] :
            if st.session_state["answered"][current_question_idx] :
                