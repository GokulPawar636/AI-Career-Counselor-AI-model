from sqlalchemy import inspect, text

from database.db import SessionLocal, engine
from database.models import Base, CareerProfile


CAREER_PROFILE_COLUMNS = {
    "user_id": "INTEGER",
    "age": "INTEGER",
    "gender": "VARCHAR",
    "city": "VARCHAR",
    "country": "VARCHAR",
    "highest_education": "VARCHAR",
    "specialization": "VARCHAR",
    "graduation_year": "INTEGER",
    "previous_job_role": "VARCHAR",
    "industry": "VARCHAR",
    "years_of_experience": "FLOAT",
    "career_gap_years": "FLOAT",
    "reason_for_gap": "TEXT",
    "technical_skills": "TEXT",
    "soft_skills": "TEXT",
    "certifications": "TEXT",
    "interested_domains": "TEXT",
    "preferred_job_type": "VARCHAR",
    "preferred_location": "VARCHAR",
    "study_hours_per_day": "FLOAT",
    "expected_salary": "VARCHAR",
    "career_goal": "TEXT",
    "resume_text": "TEXT",
    "employability_score": "FLOAT",
    "readiness_score": "FLOAT",
    "ai_report": "TEXT",
    "recommendation": "TEXT",
    "skill_gap": "TEXT",
    "roadmap": "TEXT",
}


def ensure_database_schema():
    """
    Create missing tables and add missing CareerProfile columns.
    SQLite create_all does not update existing tables, so this keeps older
    local databases compatible with the current assessment form.
    """

    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)

    if "career_profiles" not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("career_profiles")
    }

    missing_columns = {
        name: column_type
        for name, column_type in CAREER_PROFILE_COLUMNS.items()
        if name not in existing_columns
    }

    if not missing_columns:
        return

    with engine.begin() as connection:
        for name, column_type in missing_columns.items():
            connection.execute(
                text(f"ALTER TABLE career_profiles ADD COLUMN {name} {column_type}")
            )


def save_career_profile(user_id, data, ai_report):
    """
    Save the user's complete career assessment and generated AI report.
    """

    ensure_database_schema()

    db = SessionLocal()

    try:
        profile = CareerProfile(

            user_id=user_id,

            # Basic Information
            age=data.get("age"),
            gender=data.get("gender"),
            city=data.get("city"),
            country=data.get("country"),

            # Education
            highest_education=data.get("education"),
            specialization=data.get("specialization"),
            graduation_year=data.get("graduation_year"),

            # Experience
            previous_job_role=data.get("previous_job_role"),
            industry=data.get("industry"),
            years_of_experience=data.get("years_of_experience"),

            # Career Gap
            career_gap_years=data.get("career_gap"),
            reason_for_gap=data.get("reason_for_gap"),

            # Skills
            technical_skills=data.get("skills"),
            soft_skills=data.get("soft_skills"),
            certifications=data.get("certifications"),

            # Interests and Preferences
            interested_domains=data.get("interests"),
            preferred_job_type=data.get("preferred_job"),
            preferred_location=data.get("preferred_location"),
            expected_salary=data.get("expected_salary"),

            # Goal and Study Plan
            career_goal=data.get("goals"),
            study_hours_per_day=data.get("hours"),

            # Resume and AI Output
            resume_text=data.get("resume_text"),
            ai_report=ai_report

        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile

    except Exception as e:

        db.rollback()
        raise e

    finally:

        db.close()

def get_user_career_profiles(user_id, limit=5):
    """
    Return saved career reports for the logged-in user, newest first.
    """

    ensure_database_schema()

    db = SessionLocal()

    try:
        return (
            db.query(CareerProfile)
            .filter(CareerProfile.user_id == user_id)
            .order_by(CareerProfile.id.desc())
            .limit(limit)
            .all()
        )

    finally:

        db.close()
