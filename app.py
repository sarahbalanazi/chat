import streamlit as st
from fuzzywuzzy import fuzz

# App Title
st.set_page_config(page_title="AI Doc Assistant", page_icon="💊")
st.title("💊 AI Doc Assistant")
st.markdown(
    """
    Welcome to **AI Doc Assistant** — your simple chatbot for multivitamin advice.
    Ask anything related to general wellness or energy-boosting multivitamins, and I’ll do my best to help!
    """
)

# Q&A knowledge base
qa_pairs = [
    {
        "question": "Hi, I am looking for a multivitamin supplement.",
        "answer": "Hello. Looking into a multivitamin is a smart move. Let’s make sure you get the one that meets your needs."
    },
    {
        "question": "I just want something to support my general health and maybe boost my energy.",
        "answer": "That’s a great goal, you might consider NutriPlus Daily Multi—it could be a helpful option for everyday wellness."
    }
]

# Fuzzy matching function
def get_response(user_input, threshold=80):
    for qa in qa_pairs:
        score = fuzz.token_sort_ratio(user_input.lower(), qa["question"].lower())
        if score >= threshold:
            return qa["answer"]
    return "Sorry, I can only help with general multivitamin questions right now."

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Ask something about multivitamins...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    response = get_response(user_input)

    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
