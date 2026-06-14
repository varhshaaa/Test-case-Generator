# =====================================================================
# backend/main.py — FastAPI Backend Server
# Test Case Generator API
# Member 2 — Backend
# =====================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import json

# Load .env file to get GROQ_API_KEY
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Test Case Generator API", version="1.0.0")

# Allow frontend to connect — no CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client with API key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =====================================================================
# Request Model — frontend sends {"story": "...user story text..."}
# =====================================================================
class UserStory(BaseModel):
    story: str

# =====================================================================
# POST /generate — Main endpoint
# Receives user story, calls Groq AI, returns test artifacts as JSON
# =====================================================================
@app.post("/generate")
async def generate_test_cases(data: UserStory):

    # Validate input is not empty
    if not data.story.strip():
        raise HTTPException(status_code=400, detail="User story cannot be empty.")

    # Prompt sent to Groq AI (LLaMA 3 model)
    prompt = f"""
    You are a QA Engineer. Given the following user story, generate test artifacts.
    Respond ONLY with raw JSON in this exact format, no markdown, no explanation:
    {{
        "feature_name": "short feature title",
        "positive_test_cases": ["test 1", "test 2", "test 3"],
        "negative_test_cases": ["test 1", "test 2", "test 3"],
        "edge_test_cases": ["test 1", "test 2", "test 3"],
        "acceptance_criteria": ["criteria 1", "criteria 2"],
        "gherkin_scenarios": [
            {{
                "title": "Scenario title",
                "steps": ["Given ...", "When ...", "Then ..."]
            }}
        ]
    }}

    User Story:
    {data.story}
    """

    try:
        # Call Groq AI API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.15,
        )

        # Parse the JSON response from AI
        result = json.loads(response.choices[0].message.content)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI returned invalid JSON. Try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")

    # =====================================================================
    # Generate .feature file from Gherkin scenarios
    # =====================================================================
    try:
        feature_content = f"Feature: {result.get('feature_name', 'Generated Feature')}\n\n"

        for scenario in result.get("gherkin_scenarios", []):
            feature_content += f"  Scenario: {scenario.get('title', '')}\n"
            for step in scenario.get("steps", []):
                feature_content += f"    {step}\n"
            feature_content += "\n"

        # Save .feature file to disk
        feature_path = os.path.join(os.path.dirname(__file__), "output.feature")
        with open(feature_path, "w") as f:
            f.write(feature_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature file generation failed: {str(e)}")

    # Return the full result to frontend
    return result


# =====================================================================
# GET /download — Download the generated .feature file
# =====================================================================
@app.get("/download")
async def download_feature():
    feature_path = os.path.join(os.path.dirname(__file__), "output.feature")

    if not os.path.exists(feature_path):
        raise HTTPException(status_code=404, detail="No feature file found. Generate test cases first.")

    return FileResponse(
        path=feature_path,
        media_type="text/plain",
        filename="test_cases.feature"
    )


# =====================================================================
# GET / — Health check, confirms server is running
# =====================================================================
@app.get("/")
async def root():
    return {"message": "Test Case Generator API is running!", "status": "online"}


# =====================================================================
# Start server — run: python main.py
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)