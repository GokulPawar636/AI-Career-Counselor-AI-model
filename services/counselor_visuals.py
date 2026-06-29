import re
import pandas as pd
import streamlit as st
import plotly.express as px

COMMON_SKILLS = [
    "python", "sql", "excel", "powerpoint", "project", "management", "communication", "communications",
    "marketing", "sales", "data", "analysis", "leadership",
]


def _score_presence(text: str, keywords: list) -> int:
    text_l = text.lower()
    found = sum(1 for k in keywords if k in text_l)
    return int(100 * found / (len(keywords) if keywords else 1))


def show_resume_tips(resume_text: str):
    """Render graphical resume tips based on simple heuristics."""
    if not resume_text:
        st.warning("No resume text available. Paste resume text or upload a PDF in Resume Analyzer.")
        return

    words = re.findall(r"\w+", resume_text)
    word_count = len(words)

    skill_hits = {k: (1 if k in resume_text.lower() else 0) for k in COMMON_SKILLS}
    skill_count = sum(skill_hits.values())

    contact_present = bool(re.search(r"\b(email|@)\b", resume_text.lower())) and bool(re.search(r"\b\d{6,}\b", resume_text))

    # Heuristic score
    length_score = min(100, int(word_count / 800 * 100))
    skill_score = _score_presence(resume_text, COMMON_SKILLS)
    contact_score = 100 if contact_present else 40

    overall = int((length_score * 0.3) + (skill_score * 0.5) + (contact_score * 0.2))

    st.subheader("Resume Snapshot")
    c1, c2, c3 = st.columns(3)
    c1.metric("Length (words)", word_count)
    c2.metric("Detected Key Skills", skill_count)
    c3.metric("Contact Info", "Yes" if contact_present else "Missing")

    scores = pd.DataFrame({
        "Aspect": ["Length", "Skill Coverage", "Contact Info", "Overall"],
        "Score": [length_score, skill_score, contact_score, overall]
    })

    st.plotly_chart(px.bar(scores, x="Aspect", y="Score", color="Score", range_y=[0,100], title="Resume Scores"), width='stretch')

    st.write("### Quick Improvements")
    st.write("- Add clear contact details (email and phone) at the top.")
    st.write("- List 6–10 relevant skills (use keywords from job descriptions).")
    st.write("- Add measurable achievements (use numbers where possible).")
    st.write("- Keep the resume concise (500–900 words ideal).")

    # show skill hits
    st.write("### Skill detection")
    skill_df = pd.DataFrame([{"Skill": k.title(), "Present": v} for k, v in skill_hits.items()])
    if not skill_df.empty:
        st.table(skill_df)


def show_interview_prep(context_text: str = ""):
    """Render interview prep visuals and practice questions."""
    # Heuristic readiness values
    base = 50
    if context_text:
        base += min(20, len(context_text.split()) // 50)

    readiness = {
        "Confidence": min(100, base + 10),
        "Storytelling (STAR)": min(100, base),
        "Domain Knowledge": min(100, base - 5),
        "Behavioral Prep": min(100, base + 5),
        "Mock Interview Practice": min(100, base - 10)
    }

    st.subheader("Interview Readiness")
    df = pd.DataFrame({"Metric": list(readiness.keys()), "Score": list(readiness.values())})
    st.plotly_chart(px.bar(df, x="Metric", y="Score", range_y=[0,100], title="Interview Readiness"), width='stretch')

    st.write("### Suggested Practice Questions")
    questions = [
        "Tell me about yourself and your career break.",
        "Describe a time you solved a difficult problem at work (STAR).",
        "How do you manage competing priorities?",
        "Give an example of a successful project you led.",
        "Why are you interested in this role and how will you transition?"
    ]
    for q in questions:
        st.write(f"- {q}")

    st.write("### Quick Actions")
    st.write("1. Prepare concise 60–90 second answer for 'Tell me about yourself'.")
    st.write("2. Practice 3 STAR stories with metrics.")
    st.write("3. Do 2 mock interviews with a friend or online tool this week.")


def show_learning_roadmap(hours_per_day: int = 2):
    """Render a 30/60/90 day roadmap as a timeline chart."""
    # Simple roadmap tasks
    tasks = [
        ("30 Days - Foundations", 0, 30, "Complete foundational course, update resume, 3 practice tasks"),
        ("60 Days - Projects", 31, 60, "Build a mini-portfolio project, targeted applications"),
        ("90 Days - Interviews", 61, 90, "Mock interviews, networking, applications scaling")
    ]

    df = pd.DataFrame([{"Task": t[0], "Start": t[1], "End": t[2], "Details": t[3]} for t in tasks])

    # prepare for px.timeline: need start/end as dates; convert to day offsets from today
    import datetime
    start_date = datetime.date.today()
    df['StartDate'] = df['Start'].apply(lambda d: start_date + datetime.timedelta(days=int(d)))
    df['EndDate'] = df['End'].apply(lambda d: start_date + datetime.timedelta(days=int(d)))

    fig = px.timeline(df, x_start="StartDate", x_end="EndDate", y="Task", color="Task", title="30/60/90 Day Roadmap")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, width='stretch')

    st.write("### Roadmap Details")
    for _, row in df.iterrows():
        st.write(f"**{row['Task']}**: {row['Details']}")