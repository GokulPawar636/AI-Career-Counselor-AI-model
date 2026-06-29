import re

import pandas as pd
import streamlit as st


READINESS_BANDS = [
    (0, 39, "Needs Attention"),
    (40, 69, "Developing"),
    (70, 100, "Strong"),
]


SCORE_LABELS = {
    "Employability Score": "Employability",
    "Career Readiness Score": "Career Readiness",
    "Learning Readiness Score": "Learning Readiness",
    "Skill Match Score": "Skill Match",
    "Resume Strength Score": "Resume Strength",
    "Interview Readiness Score": "Interview Readiness",
    "Confidence Score": "Confidence",
}


def extract_scores(report_text: str) -> dict:
    """Extract score values from the AI-generated markdown report."""
    if not report_text:
        return {}

    scores = {}
    normalized = report_text.replace("/100", "")

    for label in SCORE_LABELS:
        match = re.search(rf"{re.escape(label)}\s*[:\-]\s*(\d{{1,3}})", normalized, re.IGNORECASE)
        if match:
            scores[label] = int(match.group(1))

    return scores


def extract_recommendations(report_text: str) -> list:
    """Extract top career recommendations from the report."""
    if not report_text:
        return []

    matches = re.findall(r"(?i)(?:role name|recommended role|career path)\s*[:\-]\s*(.+)", report_text)
    recommendations = [match.strip().strip(".*") for match in matches if match.strip()]
    return recommendations[:3]


def extract_roadmap_sections(report_text: str) -> list:
    """Extract roadmap phases from the report."""
    if not report_text:
        return []

    headings = re.findall(r"^###\s+(.+)$", report_text, re.MULTILINE)
    return headings[:3]


def extract_action_items(report_text: str) -> list:
    """Extract action items from the final action plan section."""
    if not report_text:
        return []

    section_match = re.search(r"##\s*9\.\s*Final Action Plan(.*)", report_text, re.DOTALL | re.IGNORECASE)
    if not section_match:
        return []

    bullets = re.findall(r"^-\s+(.+)", section_match.group(1))
    return bullets[:5]


def get_readiness_band(score: int) -> str:
    """Map a score to a readable readiness band."""
    for low, high, band in READINESS_BANDS:
        if low <= score <= high:
            return band
    return "Needs Attention"


def render_report_dashboard(report_text: str) -> None:
    """Render a visual summary for the report in the dashboard."""
    if not report_text:
        st.info("No report content is available yet.")
        return

    scores = extract_scores(report_text)

    if scores:
        st.subheader("Assessment Scores")
        score_rows = [{"Metric": label, "Score": value} for label, value in scores.items()]
        score_df = pd.DataFrame(score_rows)

        overall_score = int(sum(scores.values()) / len(scores))
        top_score = max(scores.items(), key=lambda item: item[1])
        band = get_readiness_band(overall_score)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Overall Readiness", f"{overall_score}/100", band)
        col2.metric("Best Score", f"{top_score[1]}/100", top_score[0])
        col3.metric("Tracked Areas", len(scores))
        col4.metric("Readiness Level", band)

        st.dataframe(
            score_df.assign(Score=lambda df: df["Score"].astype(int)),
            width='stretch',
            hide_index=True,
        )

        st.bar_chart(score_df.set_index("Metric")["Score"], width='stretch')

        st.write("### Score Breakdown")
        for label, value in scores.items():
            st.write(f"**{label}:** {value}/100")
            st.progress(value / 100)

        st.write("### Readiness Summary")
        readiness_df = pd.DataFrame(
            {
                "Category": ["Experience", "Skills", "Learning", "Interview Prep", "Confidence"],
                "Score": [
                    scores.get("Career Readiness Score", 0),
                    scores.get("Skill Match Score", 0),
                    scores.get("Learning Readiness Score", 0),
                    scores.get("Interview Readiness Score", 0),
                    scores.get("Confidence Score", 0),
                ],
            }
        )
        st.bar_chart(readiness_df.set_index("Category")["Score"], width='stretch')

    recommendations = extract_recommendations(report_text)
    if recommendations:
        st.subheader("Suggested Career Paths")
        for index, role in enumerate(recommendations, start=1):
            with st.container():
                st.write(f"{index}. **{role}**")

    roadmap_sections = extract_roadmap_sections(report_text)
    if roadmap_sections:
        st.subheader("Learning Roadmap")
        for phase in roadmap_sections:
            st.write(f"- {phase}")

    actions = extract_action_items(report_text)
    if actions:
        st.subheader("Next Actions")
        for action in actions:
            st.write(f"- {action}")

    with st.expander("View Full Report"):
        st.markdown(report_text)
