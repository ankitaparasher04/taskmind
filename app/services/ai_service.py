import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_resume(text: str):
    prompt = f"""
    You are TaskMind AI.

    Analyze the uploaded operational document.

    Return output STRICTLY in this format:

    SUMMARY:
    - point 1
    - point 2

    ACTION ITEMS:
    - item 1
    - item 2
    - item 3

    PRIORITY:
    - High / Medium / Low

    DEADLINES:
    - deadline 1
    - deadline 2

    BLOCKERS:
    - blocker 1
    - blocker 2

    NEXT STEPS:
    - next step 1
    - next step 2

    Document:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text