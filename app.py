import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="AI Genius Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("⚠️ Добавьте ваш GEMINI_API_KEY в настройках Secrets на Streamlit Cloud!")

with st.sidebar:
    st.title("⚙️ Меню")
    if st.button("🗑️ Очистить историю чата", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Хакатон: Innovation AI Hackathon – 2026")

st.markdown('<div class="main-header">🤖 AI Genius Assistant</div>', unsafe_allow_html=True)
st.caption("Полноценный ИИ-помощник (как ChatGPT)")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я твой ИИ-ассистент. Задавай любые вопросы, пиши код или проси решить задачу — я готов помочь!"}
    ]

for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Напишите сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Думаю..."):
            try:
                response = model.generate_content(prompt)
                bot_reply = response.text
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Произошла ошибка: {e}"