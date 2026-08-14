# 🎯 JobFit --- AI Job Matching Agent

JobFit is an AI-powered job matching application that analyzes how well
a candidate's resume matches a target job description.

It uses **Retrieval-Augmented Generation (RAG)**, **semantic search**,
**text embeddings**, **Chroma vector database**, **LangChain**, and
**Google Gemini** to identify matching skills, missing skills, overall
fit, and generate a tailored cover letter.

## 🚀 Features

-   📄 Upload a PDF resume
-   💼 Enter a target job description
-   🔎 Semantic search over resume content
-   🧠 AI-powered resume/job matching
-   📊 Match score from 0--100
-   ✅ Identify matching skills
-   ⚠️ Identify missing skills
-   🤖 Generate an AI summary of candidate fit
-   ✉️ Generate a tailored cover letter
-   🎨 Interactive Streamlit interface

## 🧠 How It Works

JobFit follows a Retrieval-Augmented Generation (RAG) pipeline:

``` text
Resume PDF
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embeddings
    ↓
Chroma Vector Database
    ↓
Semantic Retrieval using Job Description
    ↓
Relevant Resume Context
    ↓
Google Gemini LLM
    ↓
AI Job-Match Analysis
    ├── Match Score
    ├── Matching Skills
    ├── Missing Skills
    ├── Overall Fit
    └── AI Summary
    ↓
Tailored Cover Letter
```

## 🔍 RAG Pipeline

### 1. Ingest

The uploaded resume PDF is converted into plain text using
`PyPDFLoader`.

### 2. Chunk

The extracted resume text is divided into smaller overlapping chunks
using LangChain's `RecursiveCharacterTextSplitter`.

-   Chunk size: 500 characters
-   Chunk overlap: 100 characters

The overlap helps preserve context between neighboring chunks.

### 3. Embed

Each resume chunk is converted into a numerical vector using Google's
embedding model.

These vectors represent the semantic meaning of the resume content.

### 4. Store

The embeddings are stored in a Chroma vector store.

### 5. Retrieve

When a job description is entered, JobFit performs semantic similarity
search to retrieve the most relevant resume chunks.

The system retrieves relevant content based on meaning rather than
relying only on exact keyword matching.

### 6. Generate

The retrieved resume context and job description are passed to Google
Gemini.

Gemini generates a structured analysis containing:

-   Match score
-   Matching skills
-   Missing skills
-   Overall fit
-   Summary

The same retrieval process is used to generate a job-specific cover
letter.

## 🛠️ Tech Stack

  Technology                       Purpose
  -------------------------------- ------------------------------------
  Python                           Core programming language
  Streamlit                        Web application interface
  LangChain                        RAG pipeline and LLM orchestration
  Google Gemini                    LLM-based analysis and generation
  Google Embeddings                Text embeddings
  Chroma                           Vector database
  PyPDFLoader                      Resume PDF extraction
  RecursiveCharacterTextSplitter   Resume chunking
  python-dotenv                    Environment variable management

## 📁 Project Structure

``` text
jobfit/
│
├── app.py
├── main.py
├── resume_agent.py
├── requirements.txt
├── README.md
└── .gitignore
```

### `app.py`

Contains the Streamlit user interface and application workflow.

### `resume_agent.py`

Contains the core AI/RAG logic:

-   Resume loading
-   Text chunking
-   Embedding generation
-   Chroma vector store creation
-   Semantic retrieval
-   Gemini-based job analysis
-   Cover letter generation

### `main.py`

Supporting project execution logic.

### `requirements.txt`

Contains the Python dependencies required to run the project.

## 🖥️ Application Workflow

### Step 1 --- Upload Resume

The user uploads their resume in PDF format.

### Step 2 --- Add Job

The user pastes the target job description.

### Step 3 --- Analyze Match

JobFit retrieves relevant resume information and compares it with the
job description.

### Step 4 --- View Results

The application displays:

-   Overall match percentage
-   Matching skills
-   Missing skills
-   Overall fit
-   AI-generated explanation

### Step 5 --- Generate Cover Letter

The application generates a tailored cover letter based on the
candidate's resume and selected job description.

## 📊 Example Result

Example analysis:

``` text
Overall Match: 85%

Matching Skills:
- Python
- LangChain
- RAG Pipelines
- LLMs
- AI Internship Experience

Skills to Improve:
- Vector Databases
- LLM APIs

Overall Fit:
Strong
```

## ⚙️ Installation

Clone the repository:

``` bash
git clone https://github.com/alishhbawaseem/jobfit.git
```

Navigate into the project:

``` bash
cd jobfit
```

Create a virtual environment:

``` bash
python -m venv venv
```

Activate the virtual environment on Windows:

``` bash
venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

``` env
GEMINI_API_KEY=your_api_key_here
```

Do **not** upload your actual API key to GitHub.

## ▶️ Run the Application

Start the Streamlit application:

``` bash
streamlit run app.py
```

The application will open at:

``` text
http://localhost:8501
```

## 🔐 Security

API keys and environment variables are kept outside the source code
using a `.env` file.

The `.env` file should be included in `.gitignore` and should never be
committed to the repository.

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

-   Retrieval-Augmented Generation (RAG)
-   Semantic search
-   Text embeddings
-   Vector databases
-   LLM integration
-   Prompt engineering
-   Document processing
-   Resume information retrieval
-   AI-powered structured analysis
-   Generative AI applications
-   Streamlit application development

## 🔮 Future Improvements

Potential improvements include:

-   Support for multiple resume formats
-   Job recommendation based on resume
-   Persistent vector database storage
-   Improved evaluation of match scores
-   Resume improvement suggestions
-   Skill-gap learning recommendations
-   User authentication
-   Cloud deployment
-   Automated job listing integration

## 👩‍💻 Author

**Alishba Waseem**

AI / Generative AI Enthusiast

GitHub: https://github.com/alishhbawaseem
