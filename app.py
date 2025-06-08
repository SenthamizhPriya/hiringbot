import streamlit as st
import hashlib, json, os, re
from dotenv import load_dotenv
from litellm import completion
from prompts.prompts_templates import generate_personal_info_prompt, generate_tech_question_prompt

load_dotenv()
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    h1 {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .chat-bubble.assistant {
        background-color: #333;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 80%;
    }
    .chat-bubble.user {
        background-color: #555;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .answer-input > div > div > textarea {
        background: transparent;
        border: 2px solid white !important;
        color: white !important;
        border-radius: 8px;
        width: 100%;
        min-height: 80px;
    }
    .stSpinner {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>TalentScout Hiring Assistant</h1>", unsafe_allow_html=True)

def anonymize(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()

def save_candidate_data(data, filename="candidates_data.json"):
    existing = json.load(open(filename)) if os.path.exists(filename) else []
    existing.append(data)
    json.dump(existing, open(filename, "w"), indent=4)

# State
if "chat" not in st.session_state:
    st.session_state.chat = []
    # Welcome bubbles
    st.session_state.chat.append(("assistant",
        "Welcome to TalentScout! We’ll have a quick, easy chat to understand your background and skills better"))
    st.session_state.step = "personal"
    st.session_state.p_step = 0
    st.session_state.personal = {}
    st.session_state.tech_q = []
    st.session_state.q_idx = 0
    st.session_state.answers = {}

# Display chat
for role, msg in st.session_state.chat:
    bubble = f'<div class="chat-bubble {role}">{msg}</div>'
    st.markdown(bubble, unsafe_allow_html=True)

# Input logic
if st.session_state.step == "personal" and st.session_state.p_step < 7:
    field = ["name", "email", "phone", "experience", "position", "location", "tech_stack"][st.session_state.p_step]
    prompt = generate_personal_info_prompt(field)
    if st.session_state.chat[-1][1] != prompt:
        st.session_state.chat.append(("assistant", prompt))
        st.rerun()

    user_resp = st.text_area("", key=f"personal_{field}", placeholder="Your answer here", help="Press Enter below")
    if user_resp:
        st.session_state.chat.append(("user", user_resp))
        st.session_state.personal[field] = user_resp.strip()
        st.session_state.p_step += 1
        
        st.rerun()

elif st.session_state.step == "personal":
    st.session_state.step = "tech"
    st.rerun()

elif st.session_state.step == "tech":
    if not st.session_state.tech_q:
        st.session_state.chat.append(("assistant", "Thanks for sharing your details! Now let’s take a quick look at your skills and go through some technical questions"))
        tech_stack = st.session_state.personal.get("tech_stack", "")
        prompt = generate_tech_question_prompt(tech_stack)
        resp = completion(
            model="ollama/llama3",
            messages=[{"role":"system","content":"You are an expert hiring agent."},
                    {"role":"user","content":prompt}],
            temperature=0.5
        )
        text = resp['choices'][0]['message']['content']
        blocks = re.split(r'\n(?=\w+:)', text)
        qs = sum([re.findall(r'\d+\.\s*(.*)', b) for b in blocks], [])
        st.session_state.tech_q = qs
        st.rerun()

    if st.session_state.q_idx < len(st.session_state.tech_q):
        q = st.session_state.tech_q[st.session_state.q_idx]
        if st.session_state.chat[-1][1] != q:
            st.session_state.chat.append(("assistant", q))
            st.rerun()

        ans = st.text_area("", key=f"ans_{st.session_state.q_idx}", placeholder="Your answer here")
        if ans:
            st.session_state.chat.append(("user", ans))
            st.session_state.answers[q] = ans
            st.session_state.q_idx += 1
            st.rerun()
    else:
        st.session_state.chat.append(("assistant", "🎉 You’ve completed the interview!"))
        save_candidate_data({
            "candidate_info": st.session_state.personal,
            "answers": st.session_state.answers
        })
