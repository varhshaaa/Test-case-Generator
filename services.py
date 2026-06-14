import os
import sys
import json
from groq import Groq
from pydantic import BaseModel, Field
from typing import List

class GherkinScenario(BaseModel):
    title: str = Field(..., description="Scenario title.")
    steps: List[str] = Field(..., description="Steps using Given, When, Then syntax.")

class GenerationResponse(BaseModel):
    feature_name: str = Field(..., description="Short title of the feature.")
    positive_test_cases: List[str] = Field(..., description="List of positive tests.")
    negative_test_cases: List[str] = Field(..., description="List of negative tests.")
    edge_test_cases: List[str] = Field(..., description="List of boundary/edge tests.")
    acceptance_criteria: List[str] = Field(..., description="List of acceptance criteria.")
    gherkin_scenarios: List[GherkinScenario] = Field(..., description="Gherkin scenarios.")

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GROQ_API_KEY.")
        self.client = Groq(api_key=self.api_key)

    def generate_test_artifacts(self, user_story: str) -> GenerationResponse:
        system_prompt = (
            "You are a Principal QA Automation Architect.\n"
            "Analyze the provided User Story and output detailed QA artifacts.\n"
            "Split into: positive test cases, negative test cases, "
            "edge test cases, acceptance criteria, and Gherkin scenarios.\n"
            "Respond ONLY with raw JSON matching this schema:\n"
            f"{json.dumps(GenerationResponse.model_json_schema())}\n"
            "No markdown, no code fences, no explanation. Pure JSON only."
        )
        user_prompt = f"Analyze this User Story:\n\"\"\"\n{user_story.strip()}\n\"\"\""

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.15,
            response_format={"type": "json_object"},
        )
        raw_json = json.loads(completion.choices[0].message.content)
        return GenerationResponse.model_validate(raw_json)

if __name__ == "__main__":
    test_story = (
        "As a customer,\n"
        "I want to reset my password,\n"
        "So that I can regain access to my account."
    )
    try:
        service = LLMService()
        result = service.generate_test_artifacts(test_story)
        print("✅ SUCCESS!")
        print(f"Feature: {result.feature_name}")
        print(f"Positive Tests: {len(result.positive_test_cases)}")
        print(f"Negative Tests: {len(result.negative_test_cases)}")
        print(f"Edge Cases: {len(result.edge_test_cases)}")
        print(f"Gherkin Scenarios: {len(result.gherkin_scenarios)}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)