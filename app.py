import streamlit as st
from database.init_db import *
import database.init_db
from agents.assessment_agent import generate_career_plan
from agents.counselor_agent import answer_career_question
from services.database_service import get_user_career_profiles, save_career_profile
from services.auth_service import login_user, register_user
from services.report_visualization import render_report_dashboard
from services.resume_service import extract_pdf_text
from services.pdf_service import generate_report_pdf
from database.db import engine
from database.models import Base

Base.metadata.create_all(bind=engine)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="SheStarts AI Career Counselor",
    page_icon="briefcase",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# Session State
# ============================================


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


def reset_user_session_state():
    for key in [
        "latest_ai_report",
        "latest_assessment_data",
        "last_resume_text",
        "counselor_last_answer",
        "counselor_last_question",
    ]:
        if key in st.session_state:
            del st.session_state[key]


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.title("SheStarts AI")

    # ==========================================
    # Show Logged-in User
    # ==========================================

    if st.session_state.logged_in:

        st.success(
            f"Welcome\n\n{st.session_state.user.full_name}"
        )

    st.markdown("---")

    # ==========================================
    # Navigation
    # ==========================================

    if st.session_state.logged_in:

        page = st.radio(
            "Navigation",
            (
                "Home",
                "Career Assessment",
                "Resume Analyzer",
                "Dashboard",
                "Career Counselor",
                "About",
                "Logout"
            ),
            index=0
        )

    else:

        page = st.radio(
            "Navigation",
            (
                "Login",
                "Register"
            ),
            index=0,
            key="auth_navigation"
        )
        if page not in ["Login", "Register"]:
            page = "Login"

    st.markdown("---")

    st.success("AI Powered Career Guidance")

# ===========================
# Page Protection
# ===========================

if (
    not st.session_state.logged_in
    and page not in ["Login", "Register"]
):
    st.warning("Please login first to continue.")
    st.stop()

# ===========================
# LOGIN PAGE
# ===========================

if page == "Login":

    st.title("Welcome Back")
    st.write("Enter your details to continue your career restart journey.")

    st.markdown("<div class='page-card'>", unsafe_allow_html=True)
    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login", width='stretch'):

        status, user = login_user(
            email,
            password
        )

        if status:

            st.session_state.logged_in = True
            st.session_state.user = user
            reset_user_session_state()
            st.session_state.page = "Home"

            st.success("Login Successful")

            st.rerun()

        else:

            st.error(user)
    st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# REGISTER PAGE
# ==========================================================

elif page == "Register":

    st.title("Create Your Account")
    st.write("Join SheStarts AI and start building your comeback career plan.")

    st.markdown("<div class='page-card'>", unsafe_allow_html=True)

    name = st.text_input("Full Name", key="register_name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register", width='stretch'):

        if password != confirm:

            st.error("Passwords do not match.")

        else:

            status, message = register_user(
                name,
                email,
                password
            )

            if status:

                st.success(message)

                st.info("Registration successful. Please login.")

            else:

                st.error(message)
    st.markdown("</div>", unsafe_allow_html=True)
elif page == "Home":

    st.title("SheStarts AI Career Counselor")
    st.write("Build an AI Career Counselor for Women Restarting Their Careers.")

    col1, col2 = st.columns([2,1])

    with col1:
        st.header("Welcome")
        st.write("This AI career restart companion helps you clarify the best path, identify skill gaps, and build a practical learning roadmap.")
        st.subheader("Fast Start")
        st.write("- Understand which career path suits your experience and goals.")
        st.write("- Use the assessment, resume analyzer, and counselor chat for focused guidance.")

    with col2:
        st.subheader("AI Career Toolkit")
        st.write("Explore tools designed for career restart planning, resume readiness, interview preparation, and employability scoring.")
        st.write("Career Planning   •   Resume Guidance   •   Interview Prep   •   Learning Roadmaps ")

    if st.button(
        "Start Career Assessment",
        width='stretch'
    ):
        st.info(
            "Please select 'Career Assessment' from the sidebar."
        )

# ==========================================================
# CAREER ASSESSMENT
# ==========================================================

elif page == "Career Assessment":

    st.title("Career Assessment")

    st.write(
        "Fill out the following information to receive personalized AI career guidance for your restart journey."
    )

    st.markdown("<div class='page-card'>", unsafe_allow_html=True)
    with st.form("career_form"):

        st.subheader("Personal Details")

        col1, col2, col3 = st.columns(3)

        with col1:

            name = st.text_input("Full Name", key="assessment_name")

            age = st.number_input(
                "Age",
                18,
                65,
                value=25
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Female",
                    "Male",
                    "Non-binary",
                    "Prefer not to say"
                ]
            )

        with col2:

            city = st.text_input("City", key="assessment_city")

            country = st.text_input(
                "Country",
                value="India"
            )

        with col3:

            education = st.selectbox(
                "Highest Education",
                [
                    "High School",
                    "Diploma",
                    "Bachelor's",
                    "Master's",
                    "PhD"
                ]
            )

            specialization = st.text_input("Specialization", key="assessment_specialization")

            graduation_year = st.number_input(
                "Graduation Year",
                1980,
                2035,
                value=2024
            )

        st.subheader("Experience and Career Break")

        col1, col2 = st.columns(2)

        with col1:

            previous_job_role = st.text_input("Previous Job Role", key="assessment_previous_job_role")

            industry = st.text_input("Previous Industry", key="assessment_industry")

            years_of_experience = st.number_input(
                "Years of Experience",
                0.0,
                40.0,
                value=0.0,
                step=0.5
            )

            experience = st.text_area(
                "Previous Work Experience"
            )

        with col2:

            career_gap = st.number_input(
                "Career Gap (Years)",
                0.0,
                30.0,
                value=0.0,
                step=0.5
            )

            reason_for_gap = st.text_area(
                "Reason for Career Gap"
            )

        st.subheader("Skills and Preferences")

        col1, col2 = st.columns(2)

        with col1:

            skills = st.text_area(
                "Technical / Current Skills"
            )

            soft_skills = st.text_area(
                "Soft Skills"
            )

            certifications = st.text_area(
                "Certifications"
            )

        with col2:

            interests = st.text_area(
                "Career Interests"
            )

            preferred_job = st.selectbox(
                "Preferred Job Type",
                [
                    "Remote",
                    "Hybrid",
                    "On-site"
                ]
            )

            preferred_location = st.text_input(
                "Preferred Work Location"
            )

            expected_salary = st.text_input(
                "Expected Salary"
            )

        st.subheader("Goals and Resume")

        col1, col2 = st.columns(2)

        with col1:

            goals = st.text_area(
                "Career Goals"
            )

            hours = st.slider(
                "Study Hours Per Day",
                1,
                8,
                2
            )

        with col2:

            resume_text = st.text_area(
                "Resume Text",
                help="Paste resume text here if available."
            )

        st.divider()

        submit = st.form_submit_button(
            "Generate Career Plan",
            width='stretch'
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submit:

        # -----------------------------
        # Basic Validation
        # -----------------------------

        if not name.strip():

            st.error("Please enter your name.")

        elif not skills.strip():

            st.error("Please enter at least one skill.")

        elif not goals.strip():

            st.error("Please enter your career goal.")

        else:

            # -----------------------------
            # Collect User Data
            # -----------------------------

            data = {

                # Personal
                "name": name,
                "age": age,
                "gender": gender,
                "city": city,
                "country": country,

                # Education
                "education": education,
                "specialization": specialization,
                "graduation_year": graduation_year,

                # Experience
                "experience": experience,
                "previous_job_role": previous_job_role,
                "industry": industry,
                "years_of_experience": years_of_experience,

                # Career Break
                "career_gap": career_gap,
                "reason_for_gap": reason_for_gap,

                # Skills
                "skills": skills,
                "soft_skills": soft_skills,
                "certifications": certifications,

                # Preferences
                "interests": interests,
                "preferred_job": preferred_job,
                "preferred_location": preferred_location,
                "expected_salary": expected_salary,

                # Goal
                "goals": goals,
                "hours": hours,

                # Resume
                "resume_text": resume_text
            }

            # -----------------------------
            # Display User Profile
            # -----------------------------

            st.success("Assessment Submitted Successfully!")

            st.subheader("User Profile")

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Name:** {name}")

                st.write(f"**Education:** {education}")

                st.write(f"**Specialization:** {specialization or 'Not provided'}")

                st.write(f"**Previous Role:** {previous_job_role or 'Not provided'}")

                st.write(f"**Career Gap:** {career_gap} Years")

                st.write(f"**Study Hours:** {hours}/Day")

            with col2:

                st.write(f"**Skills:** {skills}")

                st.write(f"**Soft Skills:** {soft_skills or 'Not provided'}")

                st.write(f"**Interests:** {interests}")

                st.write(f"**Preferred Job:** {preferred_job}")

                st.write(f"**Career Goal:** {goals}")

            st.divider()

            # -----------------------------
            # AI Processing
            # -----------------------------

            with st.spinner("AI is analyzing your profile..."):

                response = None

                try:
                    response = generate_career_plan(data)

                    if not response or str(response).startswith("Error generating career plan"):
                        raise ValueError("AI service returned an empty or failed response.")

                except Exception as e:
                    response = (
                        f"AI service is currently unavailable: {e}\n\n"
                        "Here is a practical starter plan based on your assessment:\n\n"
                        "### Suggested Career Path\n"
                        f"Based on your background in {data.get('previous_job_role') or 'your previous field'}, "
                        "roles such as Operations Coordinator, Project Coordinator, Customer Success Specialist, "
                        "or Business Analyst may be a strong fit for a confident transition.\n\n"
                        "### Skills to Build\n"
                        f"- Strengthen {data.get('skills') or 'your current skills'} with modern tools and relevant certifications.\n"
                        "- Build confidence with remote collaboration, resume tailoring, and interview preparation.\n\n"
                        "### 30/60/90-Day Roadmap\n"
                        "- 30 Days: Refresh your resume, define target roles, and complete one foundational course.\n"
                        "- 60 Days: Practice interviews, build portfolio evidence, and apply to 10-15 roles.\n"
                        "- 90 Days: Improve your profile, expand networking, and continue targeted learning.\n\n"
                        "### Employability Snapshot\n"
                        "Your transition readiness is shaped by your experience, study hours, and goal clarity. "
                        "With consistent effort, you can become job-ready within a realistic timeframe."
                    )

                st.session_state.latest_ai_report = response
                st.session_state.latest_assessment_data = data
                st.session_state.last_resume_text = data.get("resume_text", "")

                if st.session_state.get("logged_in") and st.session_state.get("user"):
                    try:
                        save_career_profile(
                            user_id=st.session_state.user.id,
                            data=data,
                            ai_report=response
                        )
                    except Exception as save_error:
                        st.warning(f"Assessment saved without persistence: {save_error}")

            # -----------------------------
            # Display AI Response
            # -----------------------------

            st.success("Career Plan Generated Successfully!")

            with st.expander(
                "View Personalized AI Career Report",
                expanded=True
            ):

                st.markdown(response)
# ==========================================================
# RESUME ANALYZER
# ==========================================================

elif page == "Resume Analyzer":


    st.title("Resume Analyzer")

    st.write("Upload a PDF resume to get career restart feedback on your experience, skills, and resume clarity.")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        try:
            resume_text = extract_pdf_text(uploaded_file)
            if not resume_text.strip():
                st.warning("The uploaded PDF did not contain readable text.")
            else:
                st.success("Resume uploaded successfully!")

                analysis_data = {
                    "name": st.session_state.user.full_name if st.session_state.get("user") else "User",
                    "resume_text": resume_text,
                    "skills": "",
                    "goals": "",
                    "previous_job_role": "",
                    "experience": "",
                    "career_gap": 0,
                    "hours": 2,
                    "education": "",
                    "specialization": "",
                    "preferred_job": "Remote",
                    "preferred_location": "",
                    "expected_salary": ""
                }

                with st.spinner("Analyzing your resume for career guidance..."):
                    report = generate_career_plan(analysis_data)

                st.subheader("Resume-Based Counselation Report")
                st.markdown(report)
                st.session_state.last_resume_text = resume_text

        except Exception as exc:
            st.error(str(exc))

# ==========================================================
# CAREER COUNSELOR CHAT
# ==========================================================

elif page == "Career Counselor":

    st.title("Career Counselor Chat")

    reports = get_user_career_profiles(
        st.session_state.user.id
    )
    latest_saved_report = reports[0] if reports else None

    col1, col2, col3 = st.columns(3)

    col1.metric("Chat Mode", "Active")
    col2.metric("Quick Advice", "Yes")
    col3.metric("Saved Reports", len(reports))

    st.markdown("---")
    with st.container():
        st.subheader("Ask Your Career Counselor")
        st.write("This chat assistant can guide you through career re-entry questions in a warm, real-time style.")
    if "counselor_last_answer" not in st.session_state:
        st.session_state.counselor_last_answer = ""
        st.session_state.counselor_last_question = ""

    counselor_question = st.text_input("Ask about your career restart, resume, confidence, interview prep, or next steps:", key="counselor_input")

    def build_counselor_context():
        context_parts = [
            f"Name: {st.session_state.user.full_name if st.session_state.get('user') else 'User'}",
        ]

        if latest_saved_report:
            context_parts.append("Latest saved profile:")
            context_parts.extend([
                f"Career goal: {latest_saved_report.career_goal or 'Not provided'}",
                f"Preferred job type: {latest_saved_report.preferred_job_type or 'Not provided'}",
                f"Preferred location: {latest_saved_report.preferred_location or 'Not provided'}",
                f"Previous role: {latest_saved_report.previous_job_role or 'Not provided'}",
                f"Industry: {latest_saved_report.industry or 'Not provided'}",
                f"Years of experience: {latest_saved_report.years_of_experience or 0}",
                f"Career gap: {latest_saved_report.career_gap_years or 0} years",
                f"Skills: {latest_saved_report.technical_skills or 'Not provided'}",
                f"Soft skills: {latest_saved_report.soft_skills or 'Not provided'}",
                f"Certifications: {latest_saved_report.certifications or 'Not provided'}",
                f"Education: {latest_saved_report.highest_education or 'Not provided'}",
                f"Specialization: {latest_saved_report.specialization or 'Not provided'}",
                f"Study hours per day: {latest_saved_report.study_hours_per_day or 0}",
                f"Expected salary: {latest_saved_report.expected_salary or 'Not provided'}",
                f"City: {latest_saved_report.city or 'Not provided'}",
                f"Country: {latest_saved_report.country or 'Not provided'}",
            ])
            if latest_saved_report.resume_text:
                resume_snippet = latest_saved_report.resume_text.strip()[:400]
                context_parts.append(f"Resume excerpt: {resume_snippet}")

        elif st.session_state.get("latest_assessment_data"):
            assessment = st.session_state.latest_assessment_data
            context_parts.append("Assessment summary:")
            context_parts.extend([
                f"Career goal: {assessment.get('goals', 'Not provided')}",
                f"Preferred job type: {assessment.get('preferred_job', 'Not provided')}",
                f"Preferred location: {assessment.get('preferred_location', 'Not provided')}",
                f"Previous role: {assessment.get('previous_job_role', 'Not provided')}",
                f"Industry: {assessment.get('industry', 'Not provided')}",
                f"Years of experience: {assessment.get('years_of_experience', 0)}",
                f"Career gap: {assessment.get('career_gap', 0)} years",
                f"Skills: {assessment.get('skills', 'Not provided')}",
                f"Soft skills: {assessment.get('soft_skills', 'Not provided')}",
                f"Certifications: {assessment.get('certifications', 'Not provided')}",
                f"Education: {assessment.get('education', 'Not provided')}",
                f"Specialization: {assessment.get('specialization', 'Not provided')}",
                f"Expected salary: {assessment.get('expected_salary', 'Not provided')}",
            ])
            if st.session_state.get("last_resume_text"):
                resume_snippet = st.session_state.last_resume_text.strip()[:400]
                context_parts.append(f"Resume excerpt: {resume_snippet}")

        return "\n".join(context_parts)

    counselor_context = build_counselor_context()

    if latest_saved_report:
        st.info("This chat will use your saved profile data to give personalized guidance.")
        with st.expander("Your latest saved profile details", expanded=False):
            st.write(f"**Career Goal:** {latest_saved_report.career_goal or 'Not provided'}")
            st.write(f"**Preferred Job Type:** {latest_saved_report.preferred_job_type or 'Not provided'}")
            st.write(f"**Preferred Location:** {latest_saved_report.preferred_location or 'Not provided'}")
            st.write(f"**Experience:** {latest_saved_report.years_of_experience or 0} years")
            st.write(f"**Career Gap:** {latest_saved_report.career_gap_years or 0} years")
            st.write(f"**Skills:** {latest_saved_report.technical_skills or 'Not provided'}")
            st.write(f"**Education:** {latest_saved_report.highest_education or 'Not provided'}")
            st.write(f"**Resume uploaded:** {'Yes' if latest_saved_report.resume_text else 'No'}")
    elif st.session_state.get("latest_assessment_data"):
        st.info("This chat will use your most recent assessment details to tailor the advice.")

    col_a, col_b = st.columns([3,1])
    with col_b:
        if st.button("Get Guidance", width='stretch'):
            if counselor_question.strip():
                answer = answer_career_question(counselor_question, counselor_context)
                st.session_state.counselor_last_answer = answer
                st.session_state.counselor_last_question = counselor_question

    st.write("Quick prompts:")
    qp1, qp2, qp3 = st.columns(3)
    if qp1.button("Resume tips"):
        answer = answer_career_question(
            "How can I improve my resume for a career restart?",
            counselor_context
        )
        st.session_state.counselor_last_answer = answer
        st.session_state.counselor_last_question = "Resume tips"
    if qp2.button("Interview prep"):
        answer = answer_career_question(
            "How should I prepare for interviews after a career break?",
            counselor_context
        )
        st.session_state.counselor_last_answer = answer
        st.session_state.counselor_last_question = "Interview prep"
    if qp3.button("Learning roadmap"):
        answer = answer_career_question(
            "Suggest a 30/60/90 day learning roadmap for a career restart.",
            counselor_context
        )
        st.session_state.counselor_last_answer = answer
        st.session_state.counselor_last_question = "Learning roadmap"

    st.markdown("---")
    if st.session_state.counselor_last_answer:
        st.subheader("Latest Counselor Response")
        st.write(f"**Question:** {st.session_state.counselor_last_question}")
        st.markdown(st.session_state.counselor_last_answer)
    else:
        st.info("Ask a question or use a quick prompt to get simple guidance.")

    if reports:
        st.info(f"You have {len(reports)} saved career report(s). Visit Dashboard to review the details.")
    else:
        st.info("No saved career reports yet. Generate a career plan from the Career Assessment or Resume Analyzer first.")


# ==========================================================
# DASHBOARD

elif page == "Dashboard":

    st.title("Career Guidance Dashboard")
    st.write("Review your latest career readiness summary, saved plans, and next actions for your restart journey.")

    reports = get_user_career_profiles(
        st.session_state.user.id
    )

    total_reports = len(reports)
    latest_report = reports[0] if reports else None
    latest_goal = latest_report.career_goal if latest_report and latest_report.career_goal else "Not available"
    resume_uploaded = bool(st.session_state.get("last_resume_text"))

    col1, col2, col3 = st.columns(3)
    col1.metric("Saved Career Plans", total_reports)
    col2.metric("Resume Status", "Uploaded" if resume_uploaded else "Missing")
    col3.metric("Latest Goal", latest_goal)

    st.markdown("---")

    if latest_report:
        st.subheader("Goal Journey Overview")
        st.write(
            "This dashboard is built to help you move from a scratch-start assessment to a practical career restart plan. "
            "It shows your latest goals, strengths, and next actions while keeping your data private and secure."
        )
        st.markdown("- Personalized career plan based on your own skills, experience, and gap.")
        st.markdown("- Resume readiness and AI guidance tailored to your profile.")
        st.markdown("- Downloadable PDF report for sharing and career planning.")
        st.markdown("- Secure access so only your account can view your saved reports.")

        st.subheader("Latest Career Plan Summary")

        summary_cols = st.columns(4)
        summary_cols[0].metric("Career Gap", f"{latest_report.career_gap_years or 0} yrs")
        summary_cols[1].metric("Experience", f"{latest_report.years_of_experience or 0} yrs")
        summary_cols[2].metric("Study Hours", f"{latest_report.study_hours_per_day or 0} / day")
        summary_cols[3].metric("Preferred Mode", latest_report.preferred_job_type or "Not set")

        st.markdown("### Progress & Guidance")
        with st.expander("Latest AI Career Readiness Insights", expanded=True):
            render_report_dashboard(latest_report.ai_report or "No AI report saved for this assessment.")

        pdf_profile = {
            "career_goal": latest_report.career_goal,
            "preferred_job_type": latest_report.preferred_job_type,
            "preferred_location": latest_report.preferred_location,
            "highest_education": latest_report.highest_education,
            "previous_job_role": latest_report.previous_job_role,
            "industry": latest_report.industry,
            "years_of_experience": latest_report.years_of_experience,
            "career_gap_years": latest_report.career_gap_years,
            "study_hours_per_day": latest_report.study_hours_per_day,
        }

        pdf_bytes = generate_report_pdf(
            user_name=st.session_state.user.full_name,
            profile=pdf_profile,
            report_text=latest_report.ai_report or ""
        )

        st.download_button(
            label="Download Latest Career Report as PDF",
            data=pdf_bytes,
            file_name="SheStartsAI_Career_Report.pdf",
            mime="application/pdf",
        )

        st.markdown("### Quick Actions")
        action_list = [
            "Review the top recommendation from your latest career plan.",
            "Update your resume with the new keywords and strengths.",
            "Practice one interview story from your previous experience.",
            "Complete one learning goal in the next 7 days."
        ]
        for action in action_list:
            st.write(f"- {action}")

        st.markdown("---")
        st.subheader("Saved Reports")
        for index, report in enumerate(reports, start=1):
            title = (
                f"Report {index} - "
                f"{report.career_goal or 'Career Plan'}"
            )
            with st.expander(title, expanded=False):
                st.write(f"**Education:** {report.highest_education or 'Not provided'}")
                st.write(f"**Previous Role:** {report.previous_job_role or 'Not provided'}")
                st.write(f"**Career Gap:** {report.career_gap_years or 0} Years")
                st.write(f"**Preferred Job Type:** {report.preferred_job_type or 'Not provided'}")
                st.write(f"**Resume uploaded:** {'Yes' if report.resume_text else 'No'}")
                if report.ai_report:
                    st.write("**Summary:**")
                    report_lines = report.ai_report.splitlines()
                    for line in report_lines[:8]:
                        if line.strip():
                            st.write(f"- {line.strip()}")
                    st.write("\nClick below to view the full report.")
                    with st.expander("View full report", expanded=False):
                        st.markdown(report.ai_report)
                else:
                    st.warning("This report has no AI summary.")
    else:
        st.info(
            "Dashboard analytics and previous reports will appear after you generate a career plan."
        )

# ==========================================================
# ABOUT
# ==========================================================

elif page == "About":

    st.title("About Project")

    st.write("""
### SheStarts AI Career Counselor

Build an AI Career Counselor for Women Restarting Their Careers

### Core Features

- Career assessment for restart readiness
- Recommended career paths and skill gap analysis
- Personalized learning roadmaps
- Employability scoring and confidence guidance
- Resume review and interview preparation

### Technology Stack

- Python
- Streamlit
- Gemini AI
- SQLAlchemy
- LangChain
- SQLite
- Plotly
- ReportLab

Build an AI Career Counselor for Women Restarting Their Careers.
""")
    
# ==========================================================
# LOGOUT
# ==========================================================

elif page == "Logout":

    st.session_state.logged_in = False
    st.session_state.user = None
    reset_user_session_state()

    st.success("Logged out successfully!")

    st.rerun()
