import os
import re
from typing import List

import streamlit as st
from PyPDF2 import PdfReader

from search import extract_keywords_from_text, filter_jobs_by_keywords


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract raw text from a PDF uploaded via Streamlit."""
    try:
        reader = PdfReader(uploaded_file)
        pages_text: List[str] = []
        for page in reader.pages:
            pages_text.append(page.extract_text() or "")
        return "\n".join(pages_text)
    except Exception:
        return ""


def derive_keywords_from_resume(resume_text: str, fallback_limit: int = 20) -> List[str]:
    """Derive simple keywords from resume text as a fallback when the user doesn't type a query.

    This is intentionally simple: collect unique words >=3 characters, dedupe, and take the first N.
    """
    if not resume_text:
        return []
    words = re.findall(r"[A-Za-z][A-Za-z+.#/-]{2,}", resume_text.lower())
    seen = set()
    keywords: List[str] = []
    for w in words:
        if w not in seen:
            seen.add(w)
            keywords.append(w)
        if len(keywords) >= fallback_limit:
            break
    return keywords


st.set_page_config(page_title="AI Career Assistant", page_icon="💼", layout="wide")

st.markdown("""
<h1 style='text-align:center'>💼 AI Career Assistant</h1>
<p style='text-align:center'>Upload your resume and get AI-powered job recommendations and cover letters!</p>
""", unsafe_allow_html=True)

st.markdown("### Upload Your Resume")
uploaded_resume = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

resume_text = ""
if uploaded_resume is not None:
    resume_text = extract_text_from_pdf(uploaded_resume)
    if resume_text:
        st.success(f"Loaded resume: {uploaded_resume.name}")
    else:
        st.warning("Could not read text from this PDF. You can still type a query below.")

st.markdown("### Career Tools")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔎 Find Job Recommendations")
    user_query = st.text_input("Search keywords (optional)", placeholder="e.g. cloud, react, android")
    if st.button("Find Matching Jobs"):
        if user_query.strip():
            keywords = extract_keywords_from_text(user_query)
        else:
            keywords = derive_keywords_from_resume(resume_text)

        results = filter_jobs_by_keywords(keywords)
        if not results:
            st.error("No matching jobs found.")
        else:
            st.success(f"Found {len(results)} job(s)")
            for job in results:
                with st.container(border=True):
                    st.markdown(f"**{job.get('job_title', 'N/A')}**")
                    st.write(job.get('company_name', 'N/A'), "·", job.get('job_location', 'N/A'))
                    st.write(job.get('job_summary', ''))
                    st.write("Employment:", job.get('job_employment_type', 'N/A'))
                    st.write("Salary:", job.get('job_base_pay_range', 'N/A'))
                    st.write("Applicants:", job.get('job_num_applicants', 'N/A'))
                    if job.get("link"):
                        st.link_button("Apply / View", job["link"], use_container_width=False)

with col2:
    st.markdown("#### ✍️ Generate Cover Letter")
    target_role = st.text_input("Target role or company", placeholder="e.g. Frontend Engineer at Acme")
    if st.button("Generate Cover Letter"):
        try:
            from langchain_groq import ChatGroq
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("GROQ_API_KEY is missing. Add it to your .env.")
            else:
                model = ChatGroq(model_name="llama-3.1-8b-instant", api_key=api_key)

                base_context = resume_text.strip() or ""
                prompt = (
                    "Using the following resume context, write a concise, professional cover letter. "
                    "Match a friendly, confident tone (not overly formal). "
                    "Avoid bullet lists. 3-5 short paragraphs.\n\n"
                    f"Target: {target_role or 'General software role'}\n\n"
                    f"Resume context:\n{base_context[:6000]}\n"
                )

                response = model.invoke(prompt)
                st.markdown("**Generated Cover Letter**")
                st.text_area("", value=response.content, height=320)
        except Exception as e:
            st.error(f"Cover letter generation failed: {e}")

st.caption("Built with Streamlit · Upload a PDF resume to get started")


