
# 🧠 TalentScout Hiring Assistant

TalentScout is an AI-powered hiring assistant built with Streamlit and LLaMA 3 (via Ollama) that simulates a warm and guided interview experience. Designed to feel like a chat-based interaction, it collects candidate information, analyzes their tech stack, and asks personalized technical questions — all in a WhatsApp-style interface.

This project combines frontend simplicity with backend intelligence to support modern recruitment efforts in a more engaging and scalable way.




##  💾Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SenthamizhPriya/hiringbot.git
cd hiringbot
```

### 2. Add the prompts_templates.py file
Save the file prompts_templates.py (containing the prompt generation functions) inside the newly created prompts/ folder:

```bash
talentscout-chatbot/
└── prompts/
    └── prompts_templates.py
```

### 3. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt

```

### 5. Setup .env file
Create a .env file in the root directory and add:

```bash
# Example
OLLAMA_API_KEY=your_api_key_if_needed
```

Ensure ollama is running locally with LLaMA 3 installed:

```bash
ollama run llama3
```

### 6. Run the app
```bash
streamlit run app.py
```




## Folder Structure

```bash
📁 talentscout-hiring-assistant
├── app.py
├── prompts/
│   └── prompt_templates.py
├── candidates_data.json
├── requirements.txt
└── .env
```

## 📖 Usage Guide

1. Start the App: Launch it via the command above.

2. Enter Personal Details: The assistant will ask for basic information (name, email, etc.) in a friendly chat format.

3. Provide Tech Stack: Mention your core technical skills like Python, SQL, ML.

4. Answer Questions: The assistant will generate two technical questions per skill and let you respond one at a time.

5. Finish Interview: At the end, you’ll get a confirmation that your interview is complete.

## 🛠️Technical Details

Frontend: Streamlit

Backend LLM: LLaMA 3 via Ollama

Language: Python 3.10+

Other Libraries:

litellm – Unified LLM interface

dotenv – For environment variables

re, json, os, hashlib – Python built-ins

## 🎨Prompt Design

### 1. Personal Info Prompts
Prompts like "What's your name?" or "Where are you currently located?" are pre-crafted and displayed one at a time. They simulate a recruiter-like tone.

### 2. Technical Question Prompt
Once the tech stack is provided, a prompt like this is sent:

“Generate two short, relevant technical interview questions for each technology the candidate mentioned: Python, SQL, and Machine Learning.”

The response is parsed and displayed as one question per turn.
## 📄 Example Output


```bash
🧠 TalentScout Hiring Assistant
Welcome to TalentScout! We’ll have a quick, easy chat to understand your background and skills better.

🤖: What position are you applying for?
👤: Data Analyst

🤖: Thanks for sharing your details! Now let’s take a quick look at your skills and go through some technical questions.
🤖: 1. How would you handle missing data in a Pandas DataFrame?
👤: I would use .fillna() or .dropna() based on the context...

```
## Lessons Learned

### 1. ❌ One-time question generation issue
Problem: Initially, only one question was generated from the first technology.

Solution: Improved prompt engineering and parsing logic to split and extract multiple questions per tech skill.

### 2. 🌀 Streamlit reruns and session state
Problem: Inputs were lost on rerun or duplicate questions appeared.

Solution: Used st.session_state to track steps, inputs, and chat history precisely and avoid redundant prompts.

### 3. 🎨 Custom chat bubble styling
Problem: Streamlit doesn't natively support persistent chat bubbles or styling.

Solution: Added custom HTML/CSS to simulate WhatsApp-like chat threads with outlined text boxes and assistant/user bubble distinction.
