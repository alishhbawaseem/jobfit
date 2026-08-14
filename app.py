import os
import hashlib
import tempfile
import html as html_lib

import streamlit as st

from resume_agent import (
    load_resume_text,
    build_vector_store,
    analyze_fit,
    generate_cover_letter,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JobFit - AI Job Matching",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #0B0F19;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 15, 25, 0);
    }

    [data-testid="stSidebar"] {
        background: #101522;
        border-right: 1px solid #20283A;
    }

    [data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ---------- SIDEBAR ---------- */

    .sidebar-logo {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .sidebar-tagline {
        color: #7E8AA3;
        font-size: 13px;
        margin-bottom: 30px;
    }

    .sidebar-info {
        background: #171D2B;
        border: 1px solid #252D40;
        border-radius: 12px;
        padding: 14px;
        margin-top: 25px;
    }

    .sidebar-info-title {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 13px;
    }

    .sidebar-info-text {
        color: #7E8AA3;
        font-size: 12px;
        margin-top: 5px;
    }


    /* ---------- HEADINGS ---------- */

    .page-title {
        font-size: 38px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .page-subtitle {
        color: #8994AA;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .section-title {
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ---------- HERO ---------- */

    .hero {
        background:
            linear-gradient(
                135deg,
                #151D30 0%,
                #101827 50%,
                #111827 100%
            );

        border: 1px solid #263149;
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 25px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero-text {
        color: #9AA6BC;
        font-size: 16px;
        line-height: 1.7;
        max-width: 720px;
    }

    .hero-highlight {
        color: #5B8CFF;
        font-weight: 700;
    }


    /* ---------- CARDS ---------- */

    .card {
        background: #121927;
        border: 1px solid #222C40;
        border-radius: 16px;
        padding: 22px;
        height: 100%;
    }

    .card-title {
        color: #FFFFFF;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .card-text {
        color: #8994AA;
        font-size: 14px;
        line-height: 1.6;
    }


    /* ---------- STATUS CARDS ---------- */

    .status-card {
        background: #121927;
        border: 1px solid #222C40;
        border-radius: 15px;
        padding: 18px;
    }

    .status-icon {
        font-size: 25px;
        margin-bottom: 8px;
    }

    .status-title {
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 700;
    }

    .status-text {
        color: #8994AA;
        font-size: 13px;
        margin-top: 4px;
    }


    /* ---------- SCORE ---------- */

    .score-container {
        background:
            linear-gradient(
                145deg,
                #141D30,
                #101724
            );

        border: 1px solid #2A3751;
        border-radius: 20px;
        padding: 35px;
        text-align: center;
        margin-bottom: 20px;
    }

    .score-label {
        color: #8C98AE;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }

    .score-number {
        color: #5B8CFF;
        font-size: 72px;
        font-weight: 900;
        line-height: 1.1;
        margin-top: 8px;
    }

    .score-good {
        color: #4ADE80;
        font-weight: 600;
        font-size: 15px;
    }

    .score-medium {
        color: #FBBF24;
        font-weight: 600;
        font-size: 15px;
    }

    .score-low {
        color: #FB7185;
        font-weight: 600;
        font-size: 15px;
    }


    /* ---------- SKILL CHIPS ---------- */

    .skill {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    .skill-match {
        background: #123321;
        border: 1px solid #245E3A;
        color: #4ADE80;
    }

    .skill-missing {
        background: #332715;
        border: 1px solid #6B4B1E;
        color: #FBBF24;
    }


    /* ---------- SUMMARY ---------- */

    .summary-box {
        background: #121927;
        border: 1px solid #222C40;
        border-left: 4px solid #5B8CFF;
        border-radius: 12px;
        padding: 20px;
        color: #B5C0D4;
        font-size: 15px;
        line-height: 1.7;
    }


    /* ---------- COVER LETTER ---------- */

    .cover-letter {
        background: #121927;
        border: 1px solid #28334A;
        border-radius: 15px;
        padding: 28px;
        color: #D7DCE6;
        font-size: 15px;
        line-height: 1.8;
        white-space: pre-wrap;
    }


    /* ---------- DIVIDER ---------- */

    .custom-divider {
        height: 1px;
        background: #222C40;
        margin: 30px 0;
    }


    /* ---------- STREAMLIT BUTTONS ---------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #33415E;
        background: #172033;
        color: #FFFFFF;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #5B8CFF;
        color: #FFFFFF;
        background: #1B2943;
    }


    /* Primary buttons */

    div.stButton > button[kind="primary"] {
        background: #4F7FFF;
        border-color: #4F7FFF;
        color: white;
    }


    /* ---------- TEXT AREA ---------- */

    textarea {
        background: #101624 !important;
        color: #E6EAF0 !important;
        border: 1px solid #2A354A !important;
        border-radius: 12px !important;
    }


    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {
        background: #101624;
        border: 1px dashed #33415E;
        border-radius: 14px;
        padding: 10px;
    }


    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background: #121927;
        border: 1px solid #222C40;
        padding: 18px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #8994AA;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "vector_store": None,
    "resume_name": None,
    "resume_hash": None,
    "resume_text": None,
    "last_result": None,
    "last_jd": "",
    "cover_letter": None,
    "page": "Dashboard",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_file_hash(uploaded_file):
    """Uploaded PDF ka unique hash banata hai."""
    return hashlib.md5(uploaded_file.getvalue()).hexdigest()


def get_score_class(score):
    if score >= 75:
        return "score-good", "Strong Match"
    elif score >= 50:
        return "score-medium", "Moderate Match"
    else:
        return "score-low", "Needs Improvement"


def reset_analysis():
    st.session_state.vector_store = None
    st.session_state.resume_name = None
    st.session_state.resume_hash = None
    st.session_state.resume_text = None
    st.session_state.last_result = None
    st.session_state.last_jd = ""
    st.session_state.cover_letter = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">🎯 JobFit</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-tagline">AI-Powered Job Matching</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    if st.button("🏠  Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.button("📄  Resume", use_container_width=True):
        st.session_state.page = "Resume"

    if st.button("💼  Job Match", use_container_width=True):
        st.session_state.page = "Job Match"

    if st.button("📊  Results", use_container_width=True):
        st.session_state.page = "Results"

    if st.button("✉️  Cover Letter", use_container_width=True):
        st.session_state.page = "Cover Letter"

    st.markdown(
        """<div class="sidebar-info"><div class="sidebar-info-title">🤖 AI Analysis</div><div class="sidebar-info-text">JobFit uses semantic search and Gemini AI to compare your resume with a job description.</div></div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="page-title">Welcome to JobFit 👋</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Find out how well your resume matches your target job.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div class="hero"><div class="hero-title">Find your perfect job match.</div><div class="hero-text">Upload your resume and paste a job description. JobFit uses <span class="hero-highlight">AI + semantic search</span> to identify your matching skills, missing skills, and overall fit.</div></div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
                """<div class="status-card"><div class="status-icon">📄</div><div class="status-title">1. Upload Resume</div><div class="status-text">Upload your PDF resume.</div></div>""",
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown(
                """<div class="status-card"><div class="status-icon">💼</div><div class="status-title">2. Add Job</div><div class="status-text">Paste the job description.</div></div>""",
                unsafe_allow_html=True,
            )

    with col3:
        st.markdown(
                """<div class="status-card"><div class="status-icon">🎯</div><div class="status-title">3. Get Your Match</div><div class="status-text">Receive AI-powered analysis.</div></div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.vector_store is not None:
        st.success(
            f"✅ Resume ready: {st.session_state.resume_name}"
        )

    if st.session_state.last_result:
        score = st.session_state.last_result["match_score"]

        st.markdown("### Latest Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Match Score", f"{score}%")

        with col2:
            st.metric(
                "Matching Skills",
                len(st.session_state.last_result["matching_skills"]),
            )

        with col3:
            st.metric(
                "Missing Skills",
                len(st.session_state.last_result["missing_skills"]),
            )

        if st.button(
            "📊 View Full Results",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.page = "Results"
            st.rerun()

    else:
        if st.button(
            "🚀 Start New Analysis",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.page = "Resume"
            st.rerun()


# ============================================================
# RESUME PAGE
# ============================================================

elif st.session_state.page == "Resume":

    st.markdown(
        '<div class="page-title">Your Resume 📄</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Upload your resume so JobFit can understand your skills and experience.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div class="card"><div class="card-title">Upload your resume</div><div class="card-text">PDF format is recommended. Your resume will be processed using semantic search for the job matching analysis.</div></div>""",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_resume = st.file_uploader(
        "Choose your resume",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_resume is not None:

        current_hash = get_file_hash(uploaded_resume)

        if st.session_state.resume_hash != current_hash:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as tmp_file:

                tmp_file.write(uploaded_resume.getbuffer())
                temp_path = tmp_file.name

            try:

                with st.status(
                    "Processing your resume...",
                    expanded=True,
                ) as status:

                    st.write("📄 Reading PDF...")
                    resume_text = load_resume_text(temp_path)

                    st.write("✂️ Splitting resume into chunks...")
                    st.write("🧠 Creating semantic embeddings...")
                    vector_store = build_vector_store(resume_text)

                    st.session_state.resume_text = resume_text
                    st.session_state.vector_store = vector_store
                    st.session_state.resume_name = uploaded_resume.name
                    st.session_state.resume_hash = current_hash

                    status.update(
                        label="Resume ready!",
                        state="complete",
                        expanded=False,
                    )

            except Exception as e:

                st.error(
                    f"Resume process karne mein masla hua: {e}"
                )

            finally:

                if os.path.exists(temp_path):
                    os.remove(temp_path)

        if st.session_state.vector_store is not None:

            st.success(
                f"✅ {uploaded_resume.name} successfully processed."
            )

            text_length = len(st.session_state.resume_text or "")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Resume Content",
                    f"{text_length:,} characters",
                )

            with col2:
                st.metric(
                    "Status",
                    "Ready",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "Continue to Job Description →",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.page = "Job Match"
                st.rerun()


# ============================================================
# JOB MATCH PAGE
# ============================================================

elif st.session_state.page == "Job Match":

    st.markdown(
        '<div class="page-title">Job Match 💼</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Paste the job description you want to compare with your resume.'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.vector_store is None:

        st.warning(
            "Please upload your resume first."
        )

        if st.button("← Go to Resume"):
            st.session_state.page = "Resume"
            st.rerun()

    else:

        st.markdown(
            f"""<div class="card"><div class="card-title">📄 Resume Ready</div><div class="card-text">{html_lib.escape(st.session_state.resume_name or "")}</div></div>""",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        job_description = st.text_area(
            "Job Description",
            value=st.session_state.last_jd,
            height=300,
            placeholder=(
                "Paste the complete job description here...\n\n"
                "Example:\n"
                "We are looking for a Flutter developer with "
                "experience in Firebase, REST APIs and Git..."
            ),
        )

        st.caption(
            f"{len(job_description):,} characters"
        )

        if st.button(
            "🔍 Analyze My Match",
            type="primary",
            use_container_width=True,
            disabled=not job_description.strip(),
        ):

            try:

                with st.status(
                    "Analyzing your job fit...",
                    expanded=True,
                ) as status:

                    st.write(
                        "🔎 Finding relevant parts of your resume..."
                    )

                    st.write(
                        "🧠 Comparing your skills with the job..."
                    )

                    result = analyze_fit(
                        st.session_state.vector_store,
                        job_description,
                    )

                    st.write(
                        "📊 Preparing your match report..."
                    )

                    st.session_state.last_result = result
                    st.session_state.last_jd = job_description
                    st.session_state.cover_letter = None

                    status.update(
                        label="Analysis complete!",
                        state="complete",
                        expanded=False,
                    )

                st.session_state.page = "Results"
                st.rerun()

            except Exception as e:

                st.error(
                    f"Analysis mein masla hua: {e}"
                )


# ============================================================
# RESULTS PAGE
# ============================================================

elif st.session_state.page == "Results":

    st.markdown(
        '<div class="page-title">Match Results 📊</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Here is how your resume compares with this job.'
        '</div>',
        unsafe_allow_html=True,
    )

    result = st.session_state.last_result

    if not result:

        st.info(
            "No analysis available yet."
        )

        if st.button("Start Analysis"):
            st.session_state.page = "Job Match"
            st.rerun()

    else:

        score = int(result["match_score"])

        score_class, score_text = get_score_class(score)

        st.markdown(
            f"""<div class="score-container"><div class="score-label">Overall Match</div><div class="score-number">{score}%</div><div class="{score_class}">{score_text}</div></div>""",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "✅ Matching Skills",
                len(result["matching_skills"]),
            )

        with col2:
            st.metric(
                "⚠️ Missing Skills",
                len(result["missing_skills"]),
            )

        with col3:
            if score >= 75:
                fit = "Strong"
            elif score >= 50:
                fit = "Moderate"
            else:
                fit = "Low"

            st.metric(
                "🎯 Overall Fit",
                fit,
            )

        st.markdown(
            '<div class="custom-divider"></div>',
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # SKILLS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Skills Analysis</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            matching_skills_html = "".join(
                f'<span class="skill skill-match">{html_lib.escape(str(skill))}</span>'
                for skill in result["matching_skills"]
            ) or '<div class="card-text">No strong matching skills identified.</div>'

            st.markdown(
                f"""<div class="card"><div class="card-title">✅ Matching Skills</div>{matching_skills_html}</div>""",
                unsafe_allow_html=True,
            )

        with col2:
            missing_skills_html = "".join(
                f'<span class="skill skill-missing">{html_lib.escape(str(skill))}</span>'
                for skill in result["missing_skills"]
            ) or '<div class="card-text">No major missing skills identified.</div>'

            st.markdown(
                f"""<div class="card"><div class="card-title">⚠️ Skills to Improve</div>{missing_skills_html}</div>""",
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">🤖 AI Summary</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""<div class="summary-box">{html_lib.escape(str(result["summary"]))}</div>""",
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # ACTIONS
        # ----------------------------------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✉️ Generate Cover Letter",
                type="primary",
                use_container_width=True,
            ):

                st.session_state.page = "Cover Letter"
                st.rerun()

        with col2:

            if st.button(
                "🔄 Analyze Another Job",
                use_container_width=True,
            ):

                st.session_state.last_result = None
                st.session_state.last_jd = ""
                st.session_state.cover_letter = None
                st.session_state.page = "Job Match"
                st.rerun()


# ============================================================
# COVER LETTER PAGE
# ============================================================

elif st.session_state.page == "Cover Letter":

    st.markdown(
        '<div class="page-title">Cover Letter ✉️</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Generate a tailored cover letter using your resume and job description.'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.vector_store is None:

        st.warning(
            "Please upload a resume first."
        )

    elif not st.session_state.last_jd:

        st.warning(
            "Please analyze a job description first."
        )

        if st.button("Go to Job Match"):
            st.session_state.page = "Job Match"
            st.rerun()

    else:

        st.markdown(
            """<div class="card"><div class="card-title">✨ AI-Tailored Cover Letter</div><div class="card-text">JobFit will use relevant information from your resume and the selected job description to create a professional cover letter.</div></div>""",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.cover_letter is None:

            if st.button(
                "✍️ Generate Cover Letter",
                type="primary",
                use_container_width=True,
            ):

                try:

                    with st.spinner(
                        "AI is writing your cover letter..."
                    ):

                        letter = generate_cover_letter(
                            st.session_state.vector_store,
                            st.session_state.last_jd,
                        )

                        st.session_state.cover_letter = letter

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Cover letter banane mein masla hua: {e}"
                    )

        else:

            st.markdown(
                '<div class="section-title">Your Cover Letter</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""<div class="cover-letter">{html_lib.escape(str(st.session_state.cover_letter))}</div>""",
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.download_button(
                label="⬇️ Download Cover Letter",
                data=st.session_state.cover_letter,
                file_name="JobFit_Cover_Letter.txt",
                mime="text/plain",
                use_container_width=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "🔄 Generate Again",
                use_container_width=True,
            ):

                st.session_state.cover_letter = None
                st.rerun()