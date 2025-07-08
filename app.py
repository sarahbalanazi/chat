import streamlit as st
from fuzzywuzzy import fuzz
import time

# Set the page configuration
st.set_page_config(page_title="AI Doc Assistant", page_icon="💊")
st.title("💊 AI Doc Assistant")

# Intro text
st.markdown(
    "Welcome to your vitamin assistant. Ask me about supplements and I’ll help you out!"
)

# Define known Q&A pairs
qa_pairs = [
    {
        "question": "Hi, I am looking for a multivitamin supplement.",
        "answer": "Hello, Looking into a multivitamin is a smart move. Let’s make sure you get the one that meets your needs.",
        "markdown": False
    },
    {
        "question": "I just want something to support my general health and maybe boost my energy.",
        "answer": "That’s a great goal, you might consider NutriPlus Daily Multi—it could be a helpful option for everyday wellness.",
        "markdown": False
    }
]

# Match user input against known questions using fuzzy logic
def get_response(user_input, threshold=70):
    for qa in qa_pairs:
        score = fuzz.token_sort_ratio(user_input.lower(), qa["question"].lower())
        if score >= threshold:
            return qa["answer"], qa.get("markdown", False)
    return "Sorry, I can only help with general multivitamin questions right now.", False

# Generator function to simulate streaming for text
def stream_text(text):
    for char in text:
        yield char
        time.sleep(0.05)  # Adjust delay for streaming effect

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("markdown", False):
            st.markdown(msg["content"])
        else:
            st.write(msg["content"])

# Accept user input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display 'typing...' simulation
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("_ AI Assistant is thinking..._")
        time.sleep(1.5)  # Simulate response delay

        # Get response and replace the placeholder
        response, is_markdown = get_response(user_input)
        typing_placeholder.empty()

        # Display response with streaming effect
        if is_markdown:
            st.markdown(response)  # Streamlit doesn't support streaming markdown directly
        else:
            st.write_stream(stream_text(response))

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "markdown": is_markdown
    })
