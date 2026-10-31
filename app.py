"""ResumeIQ - AI-powered resume analytics dashboard (Streamlit + Plotly + Pandas + Gemini Flash)."""
import json
import os
import re
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="ResumeIQ", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

PURPLE, BLUE, TEXT, MUTED = "#7C5CFF", "#2DA8FF", "#E6EAF5", "#8D9BB8"
GOOD, WARN, BAD = "#34D399", "#FBBF24", "#F87171"

# ───────────────────────────── Styling ─────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif;color:#E6EAF5}
.stApp{background:radial-gradient(900px 500px at 85% -10%,rgba(124,92,255,.16),transparent),radial-gradient(700px 400px at 10% 0%,rgba(45,168,255,.08),transparent),#0B1020}
#MainMenu,footer{visibility:hidden}
header[data-testid="stHeader"]{background:transparent}
.block-container{padding:1.6rem 2rem 3rem;max-width:1400px}
section[data-testid="stSidebar"]{background:#0A0F1D;border-right:1px solid #1B2742}
section[data-testid="stSidebar"] [data-baseweb="radio"]>div:first-child{display:none}
section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.2rem}
section[data-testid="stSidebar"] div[role="radiogroup"] label{width:100%;padding:.62rem .9rem;border-radius:12px;border:1px solid transparent;transition:all .2s;cursor:pointer}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{background:#121C31;border-color:#22304D}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:linear-gradient(135deg,#7C5CFF,#2DA8FF);box-shadow:0 6px 22px rgba(80,120,255,.35)}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:.92rem;font-weight:500;color:#C9D3EA}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#fff;font-weight:600}
.logo{display:flex;align-items:center;gap:.7rem;padding:.3rem .4rem 1.4rem}
.logo .mark{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;font-size:1.2rem;background:linear-gradient(135deg,#7C5CFF,#2DA8FF);box-shadow:0 0 22px rgba(45,168,255,.5)}
.logo b{font-size:1.2rem;letter-spacing:-.02em}
div[data-testid="stVerticalBlockBorderWrapper"]{background:#121C31;border:1px solid #22304D!important;border-radius:16px;transition:border-color .2s,box-shadow .2s}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{border-color:#34457A!important;box-shadow:0 0 0 1px rgba(124,92,255,.15),0 10px 30px rgba(0,0,0,.25)}
.ct{font-size:1rem;font-weight:600;margin:.1rem 0 .2rem}
.sub{color:#8D9BB8;font-size:.86rem}
.hdr h1{font-size:1.75rem;font-weight:700;letter-spacing:-.02em;margin:0;padding:0}
.hdr p{color:#8D9BB8;margin:.2rem 0 0;font-size:.95rem}
.icon-btn{width:42px;height:42px;border-radius:12px;background:#121C31;border:1px solid #22304D;display:grid;place-items:center;position:relative;margin:auto}
.icon-btn.dot:after{content:"";position:absolute;top:9px;right:10px;width:8px;height:8px;border-radius:50%;background:#2DA8FF;box-shadow:0 0 8px #2DA8FF}
.stat{background:linear-gradient(145deg,rgba(124,92,255,.14),rgba(45,168,255,.05) 60%),#121C31;border:1px solid #22304D;border-radius:16px;padding:1.05rem 1.15rem;transition:all .2s;height:100%}
.stat:hover{border-color:#34457A;box-shadow:0 0 24px rgba(45,168,255,.12)}
.stat .top{display:flex;justify-content:space-between;align-items:center}
.stat .lbl{color:#8D9BB8;font-size:.84rem;font-weight:500}
.stat .ic{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(124,92,255,.18);font-size:1rem}
.stat .v{font-size:2.1rem;font-weight:700;letter-spacing:-.03em;margin:.45rem 0 .15rem}
.stat .v small{font-size:1rem;color:#8D9BB8;font-weight:500}
.trend{font-size:.78rem;font-weight:600}
.sec{font-size:1.05rem;font-weight:600;margin:1.6rem 0 .6rem}
.bar{margin:.55rem 0}
.bar .row{display:flex;justify-content:space-between;font-size:.86rem;margin-bottom:.28rem}
.bar .row span:last-child{color:#8D9BB8}
.bar .track{height:7px;background:#1B2742;border-radius:8px;overflow:hidden}
.bar .fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#7C5CFF,#2DA8FF);box-shadow:0 0 10px rgba(45,168,255,.55)}
.rec{background:#121C31;border:1px solid #22304D;border-radius:16px;padding:1rem 1.1rem;height:100%;transition:all .2s}
.rec:hover{border-color:#34457A;transform:translateY(-2px)}
.rec .h{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem}
.rec .ic{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:rgba(45,168,255,.14)}
.rec b{font-size:.95rem}.rec p{color:#8D9BB8;font-size:.84rem;margin:.35rem 0 0;line-height:1.5}
.badge{display:inline-block;padding:.18rem .6rem;border-radius:999px;font-size:.74rem;font-weight:600;border:1px solid}
.b-good{color:#34D399;background:rgba(52,211,153,.1);border-color:rgba(52,211,153,.3)}
.b-warn{color:#FBBF24;background:rgba(251,191,36,.1);border-color:rgba(251,191,36,.3)}
.b-bad{color:#F87171;background:rgba(248,113,113,.1);border-color:rgba(248,113,113,.3)}
.b-info{color:#2DA8FF;background:rgba(45,168,255,.1);border-color:rgba(45,168,255,.3)}
.chip{display:inline-block;margin:.2rem .3rem .2rem 0;padding:.25rem .7rem;border-radius:999px;font-size:.8rem;background:#1B2742;border:1px solid #2A3A5E}
.chip.miss{border-color:rgba(248,113,113,.35);color:#F8B4B4}
.chip.ok{border-color:rgba(52,211,153,.35);color:#A7F3D0}
.tw{overflow-x:auto;background:#121C31;border:1px solid #22304D;border-radius:16px}
.tw table{width:100%;border-collapse:collapse;font-size:.88rem;min-width:640px}
.tw th{text-align:left;color:#8D9BB8;font-weight:500;padding:.85rem 1rem;border-bottom:1px solid #22304D}
.tw td{padding:.8rem 1rem;border-bottom:1px solid #1B2742}
.tw tr:last-child td{border-bottom:none}.tw tr:hover td{background:rgba(124,92,255,.06)}
.stButton>button,.stDownloadButton button,[data-testid="stPopover"]>button{background:linear-gradient(135deg,#7C5CFF,#2DA8FF);color:#fff;border:0;border-radius:12px;font-weight:600;padding:.55rem 1.1rem;transition:all .2s}
.stButton>button:hover,.stDownloadButton button:hover,[data-testid="stPopover"]>button:hover{box-shadow:0 6px 22px rgba(80,120,255,.45);color:#fff;border:0}
.stTextInput input,.stTextArea textarea,div[data-baseweb="select"]>div{background:#0E1628!important;border-color:#22304D!important;border-radius:12px!important;color:#E6EAF5!important}
@media(max-width:768px){.block-container{padding:1rem .9rem 2rem}.stat .v{font-size:1.7rem}.hdr h1{font-size:1.4rem}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ───────────────────────────── Sample data ─────────────────────────────
SAMPLE = {
    "ats_score": 85,
    "summary": "Strong data-science profile with solid Python and SQL depth. Quantified impact and a few role-specific keywords would lift it further.",
    "skills": {
        "Technical Skills": {"Data Analysis": 88, "Statistics": 78, "Data Visualization": 82, "Feature Engineering": 70, "Machine Learning": 65, "NLP": 60, "Deep Learning": 58},
        "Programming Languages": {"Python": 90, "SQL": 85, "C++": 75, "R": 55, "JavaScript": 45},
        "Soft Skills": {"Problem Solving": 88, "Teamwork": 84, "Communication": 80, "Time Management": 76, "Leadership": 68},
        "Tools & Technologies": {"Pandas": 90, "Excel": 80, "Plotly": 80, "Git": 78, "Streamlit": 74, "Power BI": 72, "TensorFlow": 60},
    },
    "missing_keywords": ["A/B Testing", "Docker", "AWS", "MLOps", "Scikit-learn", "Tableau", "Airflow", "CI/CD"],
    "improvement_areas": ["Professional summary", "Quantified achievements", "Job keywords", "Technical depth", "Experience wording"],
    "ats_breakdown": {"Keywords": 78, "Formatting": 92, "Content Quality": 84, "Readability": 90},
    "recommendations": [
        {"title": "Improve your professional summary", "desc": "Open with your role, years of experience and top 3 skills in two lines.", "priority": "High"},
        {"title": "Add measurable achievements", "desc": "Use numbers: 'Cut report time by 40%' beats 'Improved reporting'.", "priority": "High"},
        {"title": "Include missing job keywords", "desc": "Add terms such as A/B Testing, Docker and AWS where they truthfully apply.", "priority": "Medium"},
        {"title": "Improve technical skills", "desc": "Machine Learning and NLP score lowest. Add project evidence for both.", "priority": "Medium"},
        {"title": "Make experience descriptions stronger", "desc": "Start each bullet with an action verb and end with the result.", "priority": "Low"},
    ],
    "careers": [
        {"role": "Data Scientist", "match": 88, "why": "Python, statistics and ML projects align closely."},
        {"role": "Data Analyst", "match": 92, "why": "SQL, Excel and visualization are your strongest areas."},
        {"role": "ML Engineer", "match": 71, "why": "Needs deployment tools such as Docker and MLOps."},
        {"role": "BI Analyst", "match": 80, "why": "Power BI and dashboards are a good base."},
    ],
}
ROLE_REQ = {
    "Data Scientist": {"Python": 90, "SQL": 80, "Machine Learning": 85, "Statistics": 85, "Deep Learning": 70, "NLP": 65, "Pandas": 85, "Docker": 55},
    "Data Analyst": {"SQL": 90, "Excel": 85, "Power BI": 80, "Data Visualization": 85, "Python": 70, "Statistics": 75, "Tableau": 70},
    "ML Engineer": {"Python": 90, "Machine Learning": 90, "Deep Learning": 80, "Docker": 80, "TensorFlow": 80, "MLOps": 75, "Git": 75, "AWS": 70},
    "BI Analyst": {"SQL": 85, "Power BI": 90, "Tableau": 80, "Excel": 85, "Data Visualization": 90, "Communication": 80},
}
STATUS_KIND = {"Completed": "good", "Optimized": "info", "Needs Review": "warn", "Processing": "info"}
SAMPLE_HISTORY = pd.DataFrame({
    "Resume Name": ["Ayesha_DS_Resume.pdf", "Ayesha_Analyst_v2.pdf", "Ayesha_ML_Intern.pdf", "Ayesha_General.pdf", "Ayesha_DS_Resume_v1.pdf"],
    "Target Job": ["Data Scientist", "Data Analyst", "ML Engineer Intern", "Business Analyst", "Data Scientist"],
    "ATS Score": [85, 81, 74, 62, 68],
    "Analysis Date": ["2026-10-28", "2026-10-21", "2026-10-12", "2026-09-30", "2026-09-14"],
    "Status": ["Completed", "Optimized", "Needs Review", "Needs Review", "Completed"],
})
MONTHS = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
TREND = {"Resume score": [58, 63, 69, 74, 80, 85], "Job match": [52, 60, 64, 71, 77, 82]}

for k, v in {"data": SAMPLE, "is_sample": True, "history": SAMPLE_HISTORY.copy(), "resume_text": "", "resume_name": "",
             "target_job": "Data Scientist", "api_key": "", "model": "gemini-2.0-flash", "questions": [], "feedback": ""}.items():
    st.session_state.setdefault(k, v)


# ───────────────────────────── Helpers ─────────────────────────────
def flat_skills(d):
    return {k: v for cat in d["skills"].values() for k, v in cat.items()}


def score_kind(s):
    return "good" if s >= 80 else "warn" if s >= 65 else "bad"


def badge(text, kind):
    return f'<span class="badge b-{kind}">{text}</span>'


def stat_card(label, value, icon, trend, kind="good", suffix=""):
    color = {"good": GOOD, "bad": BAD, "warn": WARN}[kind]
    sfx = f"<small>{suffix}</small>" if suffix else ""
    return (f'<div class="stat"><div class="top"><span class="lbl">{label}</span><span class="ic">{icon}</span></div>'
            f'<div class="v">{value}{sfx}</div><div class="trend" style="color:{color}">{trend}</div></div>')


def bar_rows(items):
    return "".join(f'<div class="bar"><div class="row"><span>{n}</span><span>{p}%</span></div>'
                   f'<div class="track"><div class="fill" style="width:{p}%"></div></div></div>' for n, p in items.items())


def chips(items, kind=""):
    return "".join(f'<span class="chip {kind}">{i}</span>' for i in items) or '<span class="sub">None found</span>'


def html_table(df):
    head = "".join(f"<th>{c}</th>" for c in df.columns)
    rows = ""
    for _, r in df.iterrows():
        cells = ""
        for c in df.columns:
            v = r[c]
            if c == "Status":
                v = badge(v, STATUS_KIND.get(v, "info"))
            elif c == "ATS Score":
                v = f'<b style="color:{ {"good": GOOD, "warn": WARN, "bad": BAD}[score_kind(int(v))] }">{v}</b>/100'
            cells += f"<td>{v}</td>"
        rows += f"<tr>{cells}</tr>"
    return f'<div class="tw"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


def section(title):
    st.markdown(f'<div class="sec">{title}</div>', unsafe_allow_html=True)


def header(title, subtitle):
    c = st.columns([6, 0.6, 0.6, 2.2], vertical_alignment="center")
    c[0].markdown(f'<div class="hdr"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)
    c[1].markdown('<div class="icon-btn dot">🔔</div>', unsafe_allow_html=True)
    c[2].markdown('<div class="icon-btn">👤</div>', unsafe_allow_html=True)
    with c[3].popover("⬆️ Upload resume", use_container_width=True):
        f = st.file_uploader("PDF or TXT", type=["pdf", "txt"], key="hdr_up", label_visibility="collapsed")
        if f is not None and f.name != st.session_state.resume_name:
            text = extract_text(f)
            if text:
                st.session_state.resume_text, st.session_state.resume_name = text, f.name
        if st.session_state.resume_text:
            st.caption(f"Loaded: {st.session_state.resume_name}")
            if st.button("Analyze now", key="hdr_go"):
                run_analysis()
                st.rerun()


def mix(c1, c2, t):
    a, b = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in (c1, c2)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def style_fig(fig, h=300):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Inter", color=MUTED), legend=dict(orientation="h", y=1.12, x=0))
    return fig


def ring(score, h=290):
    n = 24
    vals = [score / n] * n + [100 - score]
    cols = [mix(PURPLE, BLUE, i / (n - 1)) for i in range(n)] + ["#1B2742"]
    fig = go.Figure(go.Pie(values=vals, marker=dict(colors=cols, line=dict(width=0)), hole=0.8, sort=False,
                           direction="clockwise", rotation=0, textinfo="none", hoverinfo="skip", showlegend=False))
    fig.add_annotation(text=f"<b>{score}%</b>", showarrow=False, font=dict(size=44, color=TEXT))
    return style_fig(fig, h)


def trend_fig(h=300):
    fig = go.Figure()
    for (name, ys), col in zip(TREND.items(), [BLUE, PURPLE]):
        fig.add_trace(go.Scatter(x=MONTHS, y=ys, mode="lines", line=dict(color=col, width=14), opacity=0.12, hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=MONTHS, y=ys, name=name, mode="lines+markers", line=dict(color=col, width=3, shape="spline"),
                                 marker=dict(size=8, color="#0B1020", line=dict(color=col, width=2)), hovertemplate="%{x}: %{y}<extra>" + name + "</extra>"))
    fig.update_xaxes(showgrid=False, linecolor="#22304D")
    fig.update_yaxes(gridcolor="#1B2742", range=[40, 100], zeroline=False)
    return style_fig(fig, h)


def chart_card(title, fig, caption=""):
    with st.container(border=True):
        st.markdown(f'<div class="ct">{title}</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        if caption:
            st.markdown(caption, unsafe_allow_html=True)


def html_card(title, body, sub=""):
    with st.container(border=True):
        st.markdown(f'<div class="ct">{title}</div>' + (f'<div class="sub">{sub}</div>' if sub else "") + body, unsafe_allow_html=True)


def compat_label(s):
    return "Excellent Resume Compatibility" if s >= 80 else "Good Resume Compatibility" if s >= 65 else "Needs Improvement"


# ───────────────────────────── AI / data logic ─────────────────────────────
def get_key():
    if st.session_state.api_key:
        return st.session_state.api_key
    try:
        return st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


def gemini(prompt, as_json=False):
    key = get_key()
    if not key:
        raise RuntimeError("No Gemini API key found. Add one in Settings or set GEMINI_API_KEY.")
    import google.generativeai as genai
    genai.configure(api_key=key)
    cfg = {"response_mime_type": "application/json"} if as_json else {}
    resp = genai.GenerativeModel(st.session_state.model).generate_content(prompt, generation_config=cfg)
    return resp.text


def extract_text(f):
    try:
        if f.name.lower().endswith(".pdf"):
            from pypdf import PdfReader
            return "\n".join(p.extract_text() or "" for p in PdfReader(f).pages).strip()
        return f.read().decode("utf-8", errors="ignore").strip()
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        return ""


def run_analysis():
    text, job = st.session_state.resume_text, st.session_state.target_job or "General role"
    if not text:
        st.warning("Upload a resume or paste its text first.")
        return
    schema = {"ats_score": 0, "summary": "", "skills": {"Technical Skills": {"skill": 0}, "Programming Languages": {"skill": 0}, "Soft Skills": {"skill": 0}, "Tools & Technologies": {"skill": 0}},
              "missing_keywords": [""], "improvement_areas": [""], "ats_breakdown": {"Keywords": 0, "Formatting": 0, "Content Quality": 0, "Readability": 0},
              "recommendations": [{"title": "", "desc": "", "priority": "High|Medium|Low"}], "careers": [{"role": "", "match": 0, "why": ""}]}
    prompt = (f"You are an expert ATS and career coach. Analyze this resume for the target job '{job}'. "
              f"Skill values are proficiency percentages (0-100). Give exactly 5 recommendations and 4 careers. "
              f"Return ONLY JSON matching this shape: {json.dumps(schema)}\n\nRESUME:\n{text[:12000]}")
    with st.spinner("Analyzing your resume with Gemini..."):
        try:
            raw = re.sub(r"^```(?:json)?|```$", "", gemini(prompt, True).strip(), flags=re.M).strip()
            parsed = json.loads(raw)
            data = {**SAMPLE, **{k: v for k, v in parsed.items() if k in SAMPLE and v}}
            data["ats_score"] = int(max(0, min(100, data["ats_score"])))
            st.session_state.data, st.session_state.is_sample = data, False
            row = pd.DataFrame([{"Resume Name": st.session_state.resume_name or "Pasted resume", "Target Job": job, "ATS Score": data["ats_score"],
                                 "Analysis Date": date.today().isoformat(), "Status": "Completed"}])
            st.session_state.history = pd.concat([row, st.session_state.history], ignore_index=True)
            st.success("Analysis complete.")
        except Exception as e:
            st.error(f"Analysis failed: {e}. Showing sample data instead.")


def job_match(jd):
    vocab = set(flat_skills(SAMPLE)) | {s for r in ROLE_REQ.values() for s in r} | set(SAMPLE["missing_keywords"])
    wanted = [s for s in sorted(vocab) if s.lower() in jd.lower()]
    have = {s.lower() for s in flat_skills(st.session_state.data)}
    got = [s for s in wanted if s.lower() in have]
    return (round(len(got) / len(wanted) * 100) if wanted else 0), got, [s for s in wanted if s not in got]


# ───────────────────────────── Pages ─────────────────────────────
def page_dashboard():
    d = st.session_state.data
    header("Welcome to ResumeIQ 👋", "Your AI-powered career intelligence dashboard.")
    if st.session_state.is_sample:
        st.caption("Showing sample data. Upload a resume to see your own analysis.")
    st.write("")
    cards = [("ATS Score", d["ats_score"], "🎯", "▲ 6 pts this month", "good", "/100"),
             ("Skills Identified", sum(len(v) for v in d["skills"].values()), "🧠", "▲ 3 new skills", "good", ""),
             ("Missing Keywords", len(d["missing_keywords"]), "🔍", "▼ 2 fewer than before", "good", ""),
             ("Improvement Areas", len(d["improvement_areas"]), "🛠️", "Review recommendations", "warn", "")]
    for col, c in zip(st.columns(4), cards):
        col.markdown(stat_card(*c), unsafe_allow_html=True)
    st.write("")
    a, b = st.columns([1, 1.6])
    with a:
        chart_card("ATS Score Overview", ring(d["ats_score"]),
                   f'<div style="text-align:center;margin-bottom:.4rem">{badge(compat_label(d["ats_score"]), score_kind(d["ats_score"]))}</div>')
    with b:
        chart_card("Resume Performance", trend_fig(), '<div class="sub">Score improvements over the last six months</div>')
    section("Skills Analysis")
    cats = list(d["skills"].items())
    for row in (cats[:2], cats[2:]):
        for col, (name, items) in zip(st.columns(2), row):
            with col:
                top = dict(sorted(items.items(), key=lambda x: -x[1])[:5])
                html_card(name, bar_rows(top))
    section("AI Recommendations")
    icons = ["✍️", "📈", "🔑", "🧩", "💬"]
    recs = d["recommendations"][:5]
    for chunk in (range(0, 3), range(3, len(recs))):
        cols = st.columns(3)
        for col, i in zip(cols, chunk):
            r = recs[i]
            kind = {"High": "bad", "Medium": "warn", "Low": "info"}.get(r.get("priority"), "info")
            col.markdown(f'<div class="rec"><div class="h"><span class="ic">{icons[i % 5]}</span>{badge(r.get("priority", "Low") + " priority", kind)}</div>'
                         f'<b>{r["title"]}</b><p>{r["desc"]}</p></div>', unsafe_allow_html=True)
        st.write("")
    section("Recent Analysis")
    st.markdown(html_table(st.session_state.history.head(5)), unsafe_allow_html=True)


def page_analyzer():
    header("Resume Analyzer", "Upload or paste your resume and get an instant AI review.")
    st.write("")
    with st.container(border=True):
        st.markdown('<div class="ct">Analyze a resume</div>', unsafe_allow_html=True)
        f = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"], key="an_up")
        if f is not None and f.name != st.session_state.resume_name:
            t = extract_text(f)
            if t:
                st.session_state.resume_text, st.session_state.resume_name = t, f.name
        st.session_state.resume_text = st.text_area("Or paste resume text", st.session_state.resume_text, height=200)
        st.session_state.target_job = st.text_input("Target job title", st.session_state.target_job)
        if st.button("Analyze resume"):
            run_analysis()
    d = st.session_state.data
    st.write("")
    a, b = st.columns([1, 1.6])
    with a:
        chart_card("ATS Score", ring(d["ats_score"]))
    with b:
        html_card("AI Summary", f'<p style="line-height:1.7">{d["summary"]}</p>' + chips(d["improvement_areas"], "miss"), "Areas to improve")


def page_ats():
    d = st.session_state.data
    header("ATS Score", "How applicant tracking systems read your resume.")
    st.write("")
    a, b = st.columns([1, 1.4])
    with a:
        chart_card("Overall score", ring(d["ats_score"]), f'<div style="text-align:center">{badge(compat_label(d["ats_score"]), score_kind(d["ats_score"]))}</div>')
    with b:
        html_card("Score breakdown", bar_rows(d["ats_breakdown"]))
        html_card("Missing keywords", chips(d["missing_keywords"], "miss"), "Add these where they honestly apply")


def page_matcher():
    header("Job Matcher", "Paste a job description to see how well you fit.")
    jd = st.text_area("Job description", height=220, placeholder="Paste the job posting here...")
    if st.button("Match my resume"):
        if not jd.strip():
            st.warning("Paste a job description first.")
        else:
            pct, got, miss = job_match(jd)
            if not (got or miss):
                st.info("No known skills were found in this description. Try a longer posting.")
            else:
                a, b = st.columns([1, 1.4])
                with a:
                    chart_card("Match score", ring(pct))
                with b:
                    html_card("Skills you have", chips(got, "ok"))
                    html_card("Skills to add", chips(miss, "miss"))


def page_gap():
    d = st.session_state.data
    header("Skill Gap Analyzer", "Compare your skills with what a role expects.")
    role = st.selectbox("Target role", list(ROLE_REQ))
    req, have = ROLE_REQ[role], {k.lower(): v for k, v in flat_skills(d).items()}
    names = list(req)
    cur = [have.get(n.lower(), 0) for n in names]
    fig = go.Figure()
    for nm, vals, col, fill in [("Required", list(req.values()), PURPLE, "rgba(124,92,255,.2)"), ("You", cur, BLUE, "rgba(45,168,255,.25)")]:
        fig.add_trace(go.Scatterpolar(r=vals + vals[:1], theta=names + names[:1], name=nm, fill="toself", fillcolor=fill, line=dict(color=col, width=2)))
    fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(range=[0, 100], gridcolor="#22304D", linecolor="#22304D"), angularaxis=dict(gridcolor="#22304D")))
    a, b = st.columns([1.2, 1])
    with a:
        chart_card("Skill coverage", style_fig(fig, 380))
    gaps = sorted(((n, req[n] - c) for n, c in zip(names, cur) if req[n] - c > 0), key=lambda x: -x[1])
    with b:
        html_card("Biggest gaps", "".join(f'<div class="bar"><div class="row"><span>{n}</span><span>-{g} pts</span></div><div class="track"><div class="fill" style="width:{min(g, 100)}%;background:linear-gradient(90deg,{PURPLE},{BAD})"></div></div></div>' for n, g in gaps[:6])
                  or '<p class="sub">No gaps. You meet every requirement for this role.</p>')


def page_careers():
    header("Career Suggestions", "Roles that fit your current skills.")
    st.write("")
    cs = sorted(st.session_state.data["careers"], key=lambda c: -c["match"])
    for i in range(0, len(cs), 2):
        for col, c in zip(st.columns(2), cs[i:i + 2]):
            col.markdown(f'<div class="rec"><div class="h"><b style="font-size:1.05rem">{c["role"]}</b>{badge(str(c["match"]) + "% match", score_kind(c["match"]))}</div>'
                         f'<div class="bar"><div class="track"><div class="fill" style="width:{c["match"]}%"></div></div></div><p>{c["why"]}</p></div>', unsafe_allow_html=True)
        st.write("")


def page_coach():
    header("Interview Coach", "Practice role-specific questions and get feedback.")
    role = st.text_input("Role", st.session_state.target_job)
    if st.button("Generate questions"):
        try:
            qs = json.loads(re.sub(r"^```(?:json)?|```$", "", gemini(f"Write 5 interview questions for a {role} based on these skills: {', '.join(flat_skills(st.session_state.data))}. Return only a JSON array of strings.", True).strip(), flags=re.M))
            st.session_state.questions = [str(q) for q in qs][:5]
        except Exception as e:
            st.warning(f"Using sample questions ({e})")
            st.session_state.questions = ["Walk me through a project you are proud of.", f"How would you evaluate a {role} model or analysis?",
                                          "How do you handle missing or messy data?", "Explain a technical idea to a non-technical stakeholder.", "Tell me about a time you disagreed with a teammate."]
    if st.session_state.questions:
        q = st.selectbox("Question", st.session_state.questions)
        ans = st.text_area("Your answer", height=160)
        if st.button("Get feedback") and ans.strip():
            try:
                st.session_state.feedback = gemini(f"Act as an interview coach. Question: {q}\nAnswer: {ans}\nGive concise feedback: strengths, gaps, and a stronger sample answer.")
            except Exception as e:
                st.session_state.feedback = f"Feedback needs a Gemini key ({e})."
        if st.session_state.feedback:
            html_card("Coach feedback", "")
            st.markdown(st.session_state.feedback)


def page_history():
    header("Analysis History", "Every resume you have analyzed.")
    df = st.session_state.history
    status = st.selectbox("Filter by status", ["All"] + sorted(df["Status"].unique()))
    view = df if status == "All" else df[df["Status"] == status]
    st.markdown(html_table(view), unsafe_allow_html=True)
    st.write("")
    st.download_button("Download CSV", df.to_csv(index=False), "resumeiq_history.csv", "text/csv")


def page_settings():
    header("Settings", "Connect Gemini and manage your data.")
    with st.container(border=True):
        st.session_state.api_key = st.text_input("Gemini API key", st.session_state.api_key, type="password", help="Stored only for this session.")
        models = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
        st.session_state.model = st.selectbox("Model", models, index=models.index(st.session_state.model) if st.session_state.model in models else 0)
        st.markdown(badge("Key detected", "good") if get_key() else badge("No key. Sample data only", "warn"), unsafe_allow_html=True)
        if st.button("Reset to sample data"):
            for k in ("data", "is_sample", "history", "resume_text", "resume_name", "questions", "feedback"):
                st.session_state.pop(k, None)
            st.rerun()


NAV = {"🏠  Dashboard": page_dashboard, "📄  Resume Analyzer": page_analyzer, "🎯  ATS Score": page_ats, "🔗  Job Matcher": page_matcher,
       "📊  Skill Gap Analyzer": page_gap, "🧭  Career Suggestions": page_careers, "🎤  Interview Coach": page_coach,
       "🕘  Analysis History": page_history, "⚙️  Settings": page_settings}

with st.sidebar:
    st.markdown('<div class="logo"><div class="mark">🚀</div><b>ResumeIQ</b></div>', unsafe_allow_html=True)
    choice = st.radio("Navigation", list(NAV), label_visibility="collapsed")

try:
    NAV[choice]()
except Exception as e:
    st.error(f"Something went wrong: {e}")
