import streamlit as st
from config import load_config
from llm import stream_response

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="DataMind AI",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------------------------
# Load Configuration
# ----------------------------------------------------
config = load_config()
model = config["GOOGLE_MODEL"]

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------
with st.sidebar:

    st.title("🤖 DataMind AI")

    st.markdown("---")

    st.write(f"**Model:** `{model}`")

    st.write(f"**Messages:** {len(st.session_state.get('messages', []))}")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------------------------
# Main Page
# ----------------------------------------------------
st.title("🤖 DataMind AI")
st.caption("Your Personal Enterprise AI Assistant")

# ----------------------------------------------------
# Session State
# ----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------
# Display Previous Chat
# ----------------------------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------------------------------
# Chat Input
# ----------------------------------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # ---------------- User ----------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        answer = ""

        with st.chat_message("assistant"):

            placeholder = st.empty()

            placeholder.markdown("🤖 Thinking...")

            response = stream_response(st.session_state.messages)

            for chunk in response:

                if chunk.text:

                    answer += chunk.text

                    placeholder.markdown(answer + "▌")

            placeholder.markdown(answer)

        # ----------------------------------------------------
        # Save Assistant Response
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:

        st.error(f"❌ {e}")