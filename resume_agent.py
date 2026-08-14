"""
JobFit - AI Job Matching Agent
Core logic:
1. Load resume PDF
2. Split resume into chunks
3. Create embeddings
4. Store embeddings in Chroma
5. Retrieve relevant resume sections
6. Analyze job fit using Gemini
7. Generate a tailored cover letter
"""

import os
import json

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document


# ============================================================
# SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit(
        "Error: GEMINI_API_KEY nahi mila. .env file check karo."
    )


CHAT_MODEL = "gemini-3.6-flash"
EMBEDDING_MODEL = "gemini-embedding-001"


# ============================================================
# LOAD RESUME
# ============================================================

def load_resume_text(resume_path: str) -> str:
    """
    Resume PDF ya TXT file ko read karke plain text return karta hai.
    """

    if resume_path.lower().endswith(".pdf"):

        loader = PyPDFLoader(resume_path)
        pages = loader.load()

        return "\n".join(
            page.page_content
            for page in pages
        )

    else:

        with open(
            resume_path,
            "r",
            encoding="utf-8",
        ) as f:

            return f.read()


# ============================================================
# BUILD VECTOR STORE
# ============================================================

def build_vector_store(resume_text: str) -> Chroma:
    """
    RAG STEP 1-3:

    1. Resume text ko chunks mein split karta hai.
    2. Har chunk ki embedding banata hai.
    3. Embeddings ko Chroma vector store mein save karta hai.
    """

    # --------------------------------------------------------
    # STEP 1: CHUNKING
    # --------------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(resume_text)

    documents = [
        Document(page_content=chunk)
        for chunk in chunks
    ]

    # --------------------------------------------------------
    # STEP 2: EMBEDDINGS
    # --------------------------------------------------------

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key,
    )

    # --------------------------------------------------------
    # STEP 3: VECTOR STORE
    # --------------------------------------------------------

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="jobfit_resume",
        persist_directory="./chroma_db",
)

    return vector_store


# ============================================================
# ANALYZE JOB FIT
# ============================================================

def analyze_fit(
    vector_store: Chroma,
    job_description: str,
) -> dict:
    """
    RAG STEP 4-5:

    1. Job description ke basis par relevant resume chunks retrieve karta hai.
    2. Retrieved resume information + job description Gemini ko deta hai.
    3. Structured JSON analysis return karta hai.

    Returns:
        {
            "match_score": integer,
            "matching_skills": list,
            "missing_skills": list,
            "summary": string
        }
    """

    # --------------------------------------------------------
    # STEP 4: RETRIEVE
    # --------------------------------------------------------

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 6}
    )

    relevant_chunks = retriever.invoke(
        job_description
    )

    resume_context = "\n---\n".join(
        doc.page_content
        for doc in relevant_chunks
    )

    # --------------------------------------------------------
    # STEP 5: GENERATE ANALYSIS
    # --------------------------------------------------------

    llm = ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        google_api_key=api_key,
        temperature=0.3,
    )

    prompt = f"""
You are a career advisor AI.

Analyze how well this candidate's resume matches
the given job description.

RESUME EXCERPTS:
{resume_context}

JOB DESCRIPTION:
{job_description}

Evaluate:

1. Overall match score from 0 to 100.
2. Skills that match the job.
3. Skills that are missing or insufficient.
4. A short 2-3 sentence explanation.

Respond ONLY with valid JSON.

Do not use markdown.
Do not use code fences.
Do not add any text before or after the JSON.

Use exactly this structure:

{{
    "match_score": 75,
    "matching_skills": [
        "skill1",
        "skill2"
    ],
    "missing_skills": [
        "skill3",
        "skill4"
    ],
    "summary": "Short explanation of the candidate's fit."
}}
"""

    response = llm.invoke(prompt)

    raw_text = response.content.strip()

    # Gemini kabhi kabhi JSON ko ```json ... ``` mein wrap kar deta hai.
    raw_text = raw_text.replace(
        "```json",
        ""
    )

    raw_text = raw_text.replace(
        "```",
        ""
    )

    raw_text = raw_text.strip()

    try:

        result = json.loads(raw_text)

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Gemini ne valid JSON return nahi kiya.\n\n"
            f"Response:\n{raw_text}"
        ) from e

    return result


# ============================================================
# GENERATE COVER LETTER
# ============================================================

def generate_cover_letter(
    vector_store: Chroma,
    job_description: str,
) -> str:
    """
    Resume ke relevant sections aur job description ko use karke
    tailored professional cover letter generate karta hai.
    """

    # --------------------------------------------------------
    # RETRIEVE RELEVANT RESUME INFORMATION
    # --------------------------------------------------------

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 6}
    )

    relevant_chunks = retriever.invoke(
        job_description
    )

    resume_context = "\n---\n".join(
        doc.page_content
        for doc in relevant_chunks
    )

    # --------------------------------------------------------
    # GENERATE COVER LETTER
    # --------------------------------------------------------

    llm = ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        google_api_key=api_key,
        temperature=0.5,
    )

    prompt = f"""
Write a concise, professional cover letter
for this candidate.

Tailor it specifically to the job description.

Use only actual experience, skills, education,
and information present in the resume excerpts.

IMPORTANT:
Do not invent experience, qualifications,
companies, projects, or achievements.

RESUME EXCERPTS:
{resume_context}

JOB DESCRIPTION:
{job_description}

Write only the cover letter.

Do not include extra commentary.
Do not include markdown.
"""

    response = llm.invoke(prompt)

    return response.content.strip()