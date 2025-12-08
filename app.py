import streamlit as st
import google.generativeai as genai
import datetime as dt


API_KEY = "AIzaSyB3fbQwMv3obG9lvZsTBQ88_Ebn8cu3A_w"

st.set_page_config(
    page_title="StudEZ AI",
    page_icon="🎓",
    layout="centered"
)


BENNETT_UNIVERSITY = """
Bennett University quick facts:
- Location: Greater Noida, Uttar Pradesh, India.
- Mess timings:
  • Breakfast: 7:30–9:30 AM
  • Lunch: 12:00–3:00 PM
  • Snacks: 5:00–6:00 PM
  • Dinner: 8:00–10:00 PM
- Hostel:
  • Quiet hours: 10 PM–6 AM
  • Visitors allowed till 9 PM
  • Carry ID at all times
  • Night entry only with warden permission
- Contacts:
  • Mess Manager – Mr. Raghav Sharma – 98xxxxxxxx
  • Boys' Warden – Dr. Rao – 97xxxxxxxx
  • Girls' Warden – Ms. Singh – 96xxxxxxxx
- Attendance Portal: https://portal.example.edu
"""

SYSTEM_PROMPT_ADDITION = (
    "You are StudEZ AI, an assistant for Bennett University students. "
    "Answer ONLY Bennett-related queries (hostel, mess, academics, contacts, campus info). "
    "Be concise, factual, and polite. If a question is not about Bennett, reply: "
    "'I can answer Bennett-related queries only.'"
)


with st.sidebar:
    st.header("⚙️ Configuration")
    
    if API_KEY:
        st.success("API Key loaded from code.")
        api_key = API_KEY
    else:
        api_key = st.text_input("Enter Google API Key", type="password", help="Get your key from Google AI Studio")
        
    st.markdown("---")
    st.markdown("**About**\n\nStudEZ AI made by Team Famous Five.")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- AI Logic ---
def ask_ai(user_text, key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("models/gemini-2.5-flash-preview-09-2025")
        
        today = dt.datetime.now().strftime("%A, %d %b %Y")
        
        prompt = (
            f"{SYSTEM_PROMPT_ADDITION}\n\n"
            f"Date: {today}\n"
            f"Context Data:\n{BENNETT_UNIVERSITY}\n\n"
            f"User Query: {user_text}"
        )
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

st.title("🎓 StudEZ AI")
st.caption("Ask me about mess timings, hostel rules, or contacts.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add an initial greeting from the bot
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hi! Ask me Bennett University queries like 'mess timings', 'hostel rules', 'warden contact', or 'attendance portal'."
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your query here..."):
    if not api_key:
        st.warning("Please enter your Google API Key in the sidebar (or in the code) to proceed.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_ai(prompt, api_key)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})






