# AI-Powered QA Test Suite Studio

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen?style=for-the-badge&logo=streamlit)](https://test-case-generator-8atydenwp4tbujohz347ed.streamlit.app/)

> 🚀 **Live Demo Link:** [https://test-case-generator-8atydenwp4tbujohz347ed.streamlit.app/](https://test-case-generator-8atydenwp4tbujohz347ed.streamlit.app/)

---

## Team Name: Team-15

## Team Members

| Roll No | Name | Branch |
|---|---|---|
| 23U41A4233 | Lekkala Anusha | CSM |
| 23U41A0503 | Allu Varshini | CSE |
| 24U45A0417 | Lakkimsetty Lakshmi Narasimha Swamy | ECE |
| 24U45A0402 | Alla Kesava Sri Yasoda | ECE |

## Demo Video
https://drive.google.com/file/d/10zQ7WMJI5OcG51tFlQTPmhN5J9xDrhyZ/view?usp=sharing

## Category
Quality Assurance

## Title
Test Case Generator from User Story

## Business Problem
Writing test cases from user stories is slow, manual, inconsistent, and prone to missing edge cases. QA teams spend significant time manually crafting test cases that are often incomplete and miss critical edge scenarios.

## Solution
An AI-powered web application where a user pastes a user story and the system automatically generates positive test cases, negative test cases, edge test cases, acceptance criteria, and Gherkin scenarios in Given/When/Then format with a downloadable .feature file compatible with Cucumber and Behave.

---

## 🚀 Key Features & Capabilities
*   **Positive Test Generation:** Validates standard user journeys (happy paths) to ensure features work correctly under normal conditions.
*   **Negative Test Generation:** Checks input validation rules, invalid data boundaries, and error feedback responses.
*   **Edge & Boundary Suite:** Targets stress conditions, extreme values, character caps, and empty payloads to ensure application resilience.
*   **Agile Acceptance Criteria:** Automates definition-of-done criteria to establish baseline sprint expectations.
*   **Gherkin BDD specs:** Compiles scenarios into standard Given/When/Then templates.
*   **One-click Download:** Exports compiled Gherkin files in standard `.feature` format.

---

## 📖 Business Scenario Case Study
### Input requirement:
> *"As a shopper, I want to add products to my cart so that I can purchase them later."*

### Automatically Generated Artifacts:
1.  **Positive Case:** Add in-stock product ➔ Cart badge count increments.
2.  **Negative Case:** Add out-of-stock product ➔ Warning alert displays.
3.  **Edge Case:** Add quantity exceeding stock ceiling limit ➔ Caps quantity amount.
4.  **BDD Scenario:**
    ```gherkin
    Feature: Shopping Cart Management
      Scenario: Successful add-to-cart flow
        Given the shopper is viewing an in-stock product
        When the shopper clicks the "Add to Cart" button
        Then the product is added to the cart
        And the cart badge increments by 1
    ```

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

| Category | Technology | Description |
|---|---|---|
| Frontend | Python, Streamlit | Lightweight, responsive web interface |
| Backend | Python, FastAPI | High-performance asynchronous API services |
| LLM | LLaMA 3.3-70B via Groq API | Token completion speed >500 tokens/sec |
| Testing | Pytest | Automated endpoint verification checks |
| Source Control | GitHub | Collaborative codebase synchronization |

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

Create a `.env` file inside the `backend` folder using the provided `.env.example` file as a reference:

```env
GROQ_API_KEY=your_groq_api_key_here
```


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
