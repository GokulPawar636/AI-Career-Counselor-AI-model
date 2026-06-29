from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey

Base = declarative_base()


# ===========================
# USER LOGIN TABLE
# ===========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    profiles = relationship(
        "CareerProfile",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ===========================
# CAREER PROFILE TABLE
# ===========================

class CareerProfile(Base):
    __tablename__ = "career_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    # Basic Information
    age = Column(Integer)
    gender = Column(String)
    city = Column(String)
    country = Column(String)

    # Education
    highest_education = Column(String)
    specialization = Column(String)
    graduation_year = Column(Integer)

    # Experience
    previous_job_role = Column(String)
    industry = Column(String)
    years_of_experience = Column(Float)

    # Career Gap
    career_gap_years = Column(Float)
    reason_for_gap = Column(Text)

    # Skills
    technical_skills = Column(Text)
    soft_skills = Column(Text)
    certifications = Column(Text)

    # Interests
    interested_domains = Column(Text)

    # Work Preference
    preferred_job_type = Column(String)
    preferred_location = Column(String)

    # Study
    study_hours_per_day = Column(Float)

    # Salary
    expected_salary = Column(String)

    # Goal
    career_goal = Column(Text)

    # Resume
    resume_text = Column(Text)

    # AI Results
    employability_score = Column(Float)
    readiness_score = Column(Float)

    ai_report = Column(Text)
    recommendation = Column(Text)
    skill_gap = Column(Text)
    roadmap = Column(Text)

    user = relationship(
        "User",
        back_populates="profiles"
    )
