import streamlit as st
from chatbot import retrieve_stat, format_answer
from ai.planner import ai_plan

st.set_page_config(page_title="NBA AI Chatbot", page_icon="🏀")

st.title("🏀 NBA AI Chatbot")
st.caption("Ask anything about NBA stats")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask an NBA question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI planning
    plan = ai_plan(prompt)

    if "error" in plan:
        answer = "Sorry, I couldn’t understand that."
    else:
        result = retrieve_stat(
            action=plan.get("action"),
            player=plan.get("player"),
            stat=plan.get("stat"),
            season=plan.get("season", "2021-22"),
            top_n=plan.get("top_n")
        )
        answer = format_answer(result)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
