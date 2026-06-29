from services.gemini_service import ask_gemini


DEFAULT_GUIDANCE_RESPONSES = {
    "How can I improve my resume for a career restart?": (
        "Here are a few focused resume tips for career restart success:\n"
        "- Highlight transferable strengths, relevant projects, and career break learning.\n"
        "- Use clear role titles, outcomes, and keywords that match your target jobs.\n"
        "- Keep the resume concise, with a strong summary that explains your comeback story.\n"
        "- Add certifications, volunteer work, or short courses that demonstrate recent skill growth."
    ),
    "How should I prepare for interviews after a career break?": (
        "Try this interview prep approach:\n"
        "- Practice stories that connect your past experience to the role you want.\n"
        "- Explain the gap positively, focusing on what you learned or how you stayed current.\n"
        "- Research common questions for your target role and rehearse concise answers.\n"
        "- Show confidence by highlighting your readiness, transferable skills, and willingness to learn."
    ),
    "Suggest a 30/60/90 day learning roadmap for a career restart.": (
        "A simple 30/60/90 day roadmap for your restart:\n"
        "- 30 days: Refresh your resume, choose target roles, and complete one relevant course.\n"
        "- 60 days: Build a small project or portfolio item, network with professionals, and apply to roles.\n"
        "- 90 days: Refine applications, practice interviews, and keep learning with focused skill work."
    ),
}


def answer_career_question(question: str, context: str = "") -> str:
    """Answer a user question as a supportive career counselor."""
    try:
        prompt = f"""
You are SheStarts AI, a warm and practical career counselor for women restarting their careers.

Use only the user profile information below when tailoring the response. The answer must reflect the user's specific goals, experience, skills, gap, preferred role, location, education, and resume context.
If some fields are missing, make the advice practical based on the available details.
Answer the user's question in a friendly, conversational style. Give clear, practical guidance with simple steps and a supportive tone.
Do not add unrelated sections, long reports, or extra background details.
If the user asks for guidance, use short paragraphs or bullet points to make the advice easy to follow.
If the answer can be explained visually, describe the structure in plain text using labels such as Step 1, Step 2, or a short outline.

User profile data:
{context}

User question:
{question}

Respond with a helpful answer, practical next steps, and encouraging advice.
"""
        response = ask_gemini(prompt)
        if not response or not response.strip():
            raise ValueError("Empty Gemini response")
        return response
    except Exception:
        return DEFAULT_GUIDANCE_RESPONSES.get(
            question,
            "I'm here to support your career restart. Here is a practical and friendly next step you can take:\n"
            f"{question}"
        )
