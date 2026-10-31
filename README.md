# 🚀 ResumeIQ

An AI-powered resume analytics dashboard built with Streamlit, Plotly, Pandas and Google Gemini Flash. It scores a resume for ATS compatibility, maps skills, finds keyword gaps and suggests careers, all in a dark navy, purple and glowing-blue interface.

<!-- Add a screenshot: ![ResumeIQ dashboard](assets/dashboard.png) -->

## Features

| Page | What it does |
|------|--------------|
| Dashboard | ATS score, skill count, missing keywords, improvement areas, score ring, six-month trend, skill bars, AI recommendations, recent analyses |
| Resume Analyzer | Upload a PDF or TXT (or paste text), set a target job, run a Gemini analysis |
| ATS Score | Overall score, breakdown by keywords, formatting, content and readability, plus missing keywords |
| Job Matcher | Paste a job description and see matched and missing skills |
| Skill Gap Analyzer | Radar chart of your skills against a chosen role |
| Career Suggestions | Roles ranked by match percentage |
| Interview Coach | Gemini-generated questions and feedback on your answers |
| Analysis History | Filterable table of past analyses with CSV export |
| Settings | Gemini API key, model choice, reset to sample data |

Realistic sample data is shown until you analyze a resume, so the dashboard is never empty.

## Tech stack

- **Streamlit** for the interface and navigation
- **Plotly** for the score ring, trend line and radar charts
- **Pandas** for history and data handling
- **Gemini Flash** (`google-generativeai`) for resume analysis, interview questions and feedback
- **pypdf** for PDF text extraction
- Custom CSS for the dark SaaS styling

## Getting started

```bash
git clone https://github.com/<your-username>/resumeiq.git
cd resumeiq
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey), then provide it in one of three ways:

1. Paste it in the app under **Settings** (kept for the session only).
2. Set an environment variable: `export GEMINI_API_KEY="your_key"`
3. Add it to `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_key"
   ```

Run the app:

```bash
streamlit run app.py
```

## Project structure

```
resumeiq/
├── app.py            # Dashboard, pages, AI logic and styling
├── requirements.txt
└── README.md
```

## How the analysis works

1. The resume text is extracted from the uploaded file.
2. Gemini receives the text and the target job, and returns structured JSON: ATS score, skills with proficiency, missing keywords, recommendations and career matches.
3. The app merges the response with default values, so a partial reply never breaks the UI.
4. If the key is missing or the call fails, the app shows an error and keeps displaying sample data.

## Notes

- The six-month performance chart and the trend labels on the stat cards are sample values.
- Job Matcher runs locally by keyword overlap and does not call Gemini.
- Resume text is sent to the Gemini API when you run an analysis. Avoid uploading resumes with sensitive personal data you don't want shared.
- Never commit `.streamlit/secrets.toml` or your API key. Add it to `.gitignore`.

## Future improvements

- Store analysis history persistently (SQLite)
- Track real score trends across uploads
- DOCX resume support
- Export a PDF report

## License

MIT# resumeiq-ai-resume-analyzer
