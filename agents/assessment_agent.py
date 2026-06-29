from prompts.prompts import career_prompt
from services.gemini_service import ask_gemini


def generate_career_plan(user_data: dict) -> str:
    """
    Generate an AI-powered personalized career plan.

    Args:
        user_data (dict): User assessment information.

    Returns:
        str: AI-generated career guidance report.
    """

    try:

        prompt = career_prompt.format(
            name=user_data.get("name", ""),
            age=user_data.get("age", ""),
            gender=user_data.get("gender", ""),
            city=user_data.get("city", ""),
            country=user_data.get("country", ""),
            education=user_data.get("education", ""),
            specialization=user_data.get("specialization", ""),
            graduation_year=user_data.get("graduation_year", ""),
            experience=user_data.get("experience", ""),
            previous_job_role=user_data.get("previous_job_role", ""),
            industry=user_data.get("industry", ""),
            years_of_experience=user_data.get("years_of_experience", ""),
            career_gap=user_data.get("career_gap", ""),
            reason_for_gap=user_data.get("reason_for_gap", ""),
            skills=user_data.get("skills", ""),
            soft_skills=user_data.get("soft_skills", ""),
            certifications=user_data.get("certifications", ""),
            interests=user_data.get("interests", ""),
            preferred_job=user_data.get("preferred_job", ""),
            preferred_location=user_data.get("preferred_location", ""),
            expected_salary=user_data.get("expected_salary", ""),
            goals=user_data.get("goals", ""),
            hours=user_data.get("hours", ""),
            resume_text=user_data.get("resume_text", "")
        )

        response = ask_gemini(prompt)

        return response

    except Exception as e:

        return f"Error generating career plan: {str(e)}"