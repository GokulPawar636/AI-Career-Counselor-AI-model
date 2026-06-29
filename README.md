# SheStarts AI Career Counselor

## Overview
SheStarts AI Career Counselor is a Streamlit-based AI/ML project designed to help women restart their careers after career breaks caused by family responsibilities, childcare, relocation, marriage, or personal circumstances. The project uses Google Gemini AI for text generation and SQLAlchemy/SQLite for persistence.

This project is designed to provide:
- Career assessment for restart readiness
- Recommended career paths and skill gap analysis
- Personalized learning roadmaps
- Resume-based guidance
- Employability and confidence assessment
- A conversational career counselor chat interface

The solution uses Google Gemini AI for text generation and SQLAlchemy/SQLite for persistence.

## Core Motivation
The main objective is to deliver an AI-powered career counselor that helps users understand:
- Which career path suits them
- What skills they need
- How difficult the transition will be
- How long it may take
- What learning roadmap they should follow


## Features
- Login/Register flow with user session management
- Career Assessment form capturing education, experience, career gap, skills, goals, and preferences
- AI-generated career plan and report
- Resume upload and PDF text extraction for resume-based analysis
- Built-in goal overview and restart roadmap for users starting from scratch
- Downloadable, professionally formatted PDF of the latest career report
- Profile-aware Career Counselor chat assistant that uses the logged-in user's saved profile and assessment data
- Quick prompt guidance that also leverages profile context for tailored advice
- Dashboard with saved report summaries, actions, and private user-only access
- Visual report extraction from AI output

## New Feature
- Goal Journey Overview: A scratch-start feature that highlights essential milestones, guidance, and next steps to reach your career goal.
- Downloadable PDF report: Export the latest AI career guidance in a polished PDF format using a reusable service.
- Profile-aware Career Counselor: Chat answers are tailored using the logged-in user's saved assessment and profile details.
- Saved user data is reused across the chat and dashboard so guidance stays personalized.

## Project Structure
```text
SheStarts AI Career Counselor/
├── app.py                  # Main Streamlit entrypoint
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── career.db               # SQLite file storing users and reports
├── config/
│   └── config.py           # Loads GOOGLE_API_KEY
├── database/
│   ├── db.py               # SQLAlchemy engine and session setup
│   ├── init_db.py          # Database initialization helper
│   ├── models.py           # SQLAlchemy models for users and career profiles
├── agents/
│   ├── assessment_agent.py # Generates career plan prompt and calls Gemini
│   └── counselor_agent.py  # Generates counselor chat prompt and call
├── prompts/
│   └── prompts.py          # AI prompt templates and assignment-aligned report structure
├── services/
│   ├── auth_service.py     # Login and register logic
│   ├── database_service.py # Persistence and query helpers
│   ├── gemini_service.py   # Gemini API wrapper
│   ├── resume_service.py   # PDF resume extraction logic
│   ├── pdf_service.py      # Downloadable career report PDF generation
│   ├── report_visualization.py # Dashboard summary extraction and rendering
│   └── counselor_visuals.py # Resume / interview / learning helper visuals
└── pages/
    └── login.py            # Optional login page layout (not primary app flow)
```

## File Responsibilities
- `app.py`: Core Streamlit app controlling navigation and page rendering.
- `config/config.py`: Loads environment variables, including `GOOGLE_API_KEY`.
- `database/db.py`: Database engine, session, and SQLAlchemy initialization.
- `database/models.py`: Defines `User` and `CareerProfile` database tables.
- `database/init_db.py`: Initializes the SQLite schema if needed.
- `services/auth_service.py`: Handles user authentication and registration.
- `services/database_service.py`: Saves and retrieves career profiles, extends schema for compatibility.
- `services/gemini_service.py`: Calls the Google Gemini generative model.
- `services/resume_service.py`: Extracts text from uploaded PDF resumes.
- `services/report_visualization.py`: Parses AI report text and renders dashboard summaries.
- `services/pdf_service.py`: Generates downloadable career report PDFs with improved layout.
- `services/counselor_visuals.py`: Builds supporting visuals for resume tips, interview prep, and roadmaps.
- `agents/assessment_agent.py`: Builds the assessment prompt and gets the career plan from Gemini.
- `agents/counselor_agent.py`: Builds the chat prompt and gets counselor responses, using saved profile context for personalization.
- `prompts/prompts.py`: Contains the report template and assignment-specific prompt instructions.

## System Diagram
```text
User -> Streamlit App (app.py)
          ├── Authentication (services/auth_service.py)
          ├── Career Assessment -> agents/assessment_agent.py -> services/gemini_service.py
          ├── Resume Analyzer -> services/resume_service.py -> agents/assessment_agent.py
          ├── Career Counselor Chat -> agents/counselor_agent.py -> services/gemini_service.py
          ├── Dashboard -> services/database_service.py + services/report_visualization.py
          └── Prompt definitions -> prompts/prompts.py

Database:
  SQLite career.db stores users and career profiles via SQLAlchemy models.
```

## Installation and Setup
1. Clone the repository or copy the project folder.
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the environment:
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows CMD:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root with your Google API key:
   ```text
   GOOGLE_API_KEY=your_google_api_key_here
   ```
6. Start the app:
   ```bash
   streamlit run app.py
   ```
7. Open the URL shown in the terminal (usually http://localhost:8501).

## Running on Another System
Follow these steps to port the project to a new machine:
1. Copy the full project directory.
2. Create and activate a Python virtual environment.
3. Install dependencies from `requirements.txt`.
4. Create `.env` and add `GOOGLE_API_KEY`.
5. Ensure the system has access to the `career.db` file or allow the app to create a new SQLite database.
6. Run `streamlit run app.py`.

### Notes for Porting
- If you switch to a different AI provider, update `services/gemini_service.py` and adjust prompts in `prompts/prompts.py`.
- If you use another database, update `database/db.py` and `services/database_service.py`.
- `app.py` is the main entrypoint. Keep navigation and page structure there.

## How the Project Works
1. User registers or logs in.
2. User completes the Career Assessment form.
3. AI generates a personalized career report using Gemini.
4. User can upload a resume for resume-based analysis.
5. User can ask the Career Counselor chat for direct guidance that is personalized using their saved profile data.
6. The Dashboard displays the latest report summary, action items, and saved reports for the logged-in user only.

## User Benefits
- Personalized career guidance for women returning to work.
- Clear recommendations on suitable career paths.
- Skill gap analysis and employability readiness.
- Learning roadmap for 30/60/90 days.
- Resume review and interview prep suggestions.
- Chat assistant for quick career questions and advice.

## Development Notes
- `prompts/prompts.py` contains the AI report structure and is central to the assignment alignment.
- `agents/assessment_agent.py` and `agents/counselor_agent.py` customize AI behavior for assessment and chat; the counselor uses saved profile context to tailor responses.
- `services/report_visualization.py` builds dashboard summaries from AI output.
- `services/pdf_service.py` formats PDF exports for better readability and layout.
- `database_service.py` ensures older SQLite schema compatibility when saving new fields.

## Future Improvements
Possible next steps and enhancements:
- Add explicit employability score calculations in the saved profile.
- Add more structured resume parsing and keyword matching.
- Add multi-agent workflows or a job search assistant.
- Add user profile editing and history comparisons.
- Add deeper user profile analytics and historical trend comparison charts.
- Add more secure authentication and role-based access controls.
- Add exportable PDF/summary reports and progress tracking.

## Limitations
Current limitations of the project:
- AI recommendations depend on Gemini responses and may vary in accuracy.
- Resume analysis is based on text extraction only and does not fully validate formatting or experience context.
- The database is SQLite-based and may not scale for large user populations.
- The app currently does not include advanced security hardening or enterprise-grade authentication.
- Report parsing is heuristic and may miss information for unusually formatted AI output.

## Notes
- The main app flow is controlled from `app.py`.
- The project uses Google Gemini via `google-generativeai`; update API credentials in `.env`.

---