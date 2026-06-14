# AI-Powered QA Test Suite Studio

## Team Name: Team-15

## Team Members

| Roll No | Name | Branch |
|---|---|---|
| 23U41A4233 | Lekkala Anusha | CSM |
| 23U41A0503 | Allu Varshini | CSE |
| 24U45A0417 | Lakkimsetty Lakshmi Narasimha Swamy | ECE |
| 24U45A0402 | Alla Kesava Sri Yasoda | ECE |

## Demo Video


## Category
Quality Assurance

## Title
Test Case Generator from User Story

## Business Problem
Writing test cases from user stories is slow, manual, inconsistent, and prone to missing edge cases. QA teams spend significant time manually crafting test cases that are often incomplete and miss critical edge scenarios.

## Solution
An AI-powered web application where a user pastes a user story and the system automatically generates positive test cases, negative test cases, edge test cases, acceptance criteria, and Gherkin scenarios in Given/When/Then format with a downloadable .feature file compatible with Cucumber and Behave.

---

## Architecture Overview

```
User Story Input (Streamlit UI)
        |
        v
Backend API (FastAPI - main.py)
        |
        v
LLM Service (services.py - Groq LLaMA 3)
        |
        v
Structured JSON Response
        |
        v
Display Results in UI
        |
        v
Download .feature file
```

---

## Tech Stack

| Category | Technology |
|---|---|
| Frontend | Python, Streamlit |
| Backend | Python, FastAPI |
| LLM | LLaMA 3.3-70B via Groq API |
| Testing | Pytest |
| Source Control | GitHub |

---

## Setup Instructions

### Prerequisites
- Python 3.12 or above
- Groq API Key (free at console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/varhshaaa/Test-case-Generator.git
cd Test-case-Generator

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### Environment Setup

Create a .env file inside the backend folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## Run Instructions

### Step 1 - Start Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

Backend runs at: http://127.0.0.1:8000

### Step 2 - Start Frontend (open a new terminal)

```bash
cd ..
python -m streamlit run app.py
```

Frontend runs at: http://localhost:8501

### Step 3 - Use the Application

1. Open browser at http://localhost:8501
2. Paste a user story in the input text area
3. Click the Generate button
4. View results in Test Cases, Acceptance Criteria, and Gherkin Specs tabs
5. Download the .feature file

### Run Tests

```bash
cd backend
python -m pytest test_main.py -v
```

---

## Repository Structure

```
Test-case-Generator/
    backend/
        main.py            FastAPI backend server
        services.py        LLM service layer
        requirements.txt   Backend dependencies
        test_main.py       Pytest test cases
        output.feature     Generated feature file sample
    app.py                 Streamlit frontend
    requirements.txt       Project dependencies
    sample_data/           Sample inputs and outputs
    resumes/               Team member resumes
    ai_usage_note.md       AI usage documentation
    .gitignore
    README.md
```

---

## Assumptions and Limitations

### Assumptions
- User provides well-formed user stories in standard Agile format
- Groq API free tier is sufficient for demonstration purposes
- Python 3.12 or above is installed on the system

### Limitations
- Requires active internet connection for Groq API calls
- Free tier Groq API has rate limits
- Currently supports English language user stories only
- No persistent storage of generated test cases
