def generate_tech_question_prompt(tech_stack: str) -> str:
    """
    Prompt LLaMA to return 2 concise technical questions per technology.
    """
    return f"""
You are an expert hiring agent. The candidate has experience in the following technologies:

{tech_stack}

For each technology mentioned, ask exactly **two concise and relevant technical interview questions** to assess basic proficiency.

Format:
Technology: <Tech Name>
1. <Question 1>
2. <Question 2>

Return only questions, nothing else.
"""

def generate_personal_info_prompt(field_name):
    templates = {
        "name": "Let's begin. What's your full name?",
        "email": "Thanks! Could you share your email address?",
        "phone": "Got it. What’s your phone number?",
        "experience": "Nice. How many years of experience do you have?",
        "position": "What position are you applying for?",
        "location": "Where are you currently based?",
        "tech_stack": "Finally, list your tech stack (languages, frameworks, tools):"
    }
    return templates.get(field_name, f"Please enter your {field_name}.")
