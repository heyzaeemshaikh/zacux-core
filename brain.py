import os
import json
from groq import Groq

# Secret key se automatic connect hoga
api_key = os.environ.get("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")

if not api_key:
    print("[ERROR] GROQ_API_KEY missing!")
    exit(1)

client = Groq(api_key=api_key)

def run_zacux_brain():
    prompt = """
    You are the Autonomous Brain of ZACUX.
    Analyze digital market trends and autonomously decide on ONE profitable micro-task to execute right now.
    Categories:
    - Micro Web Utility Tool
    - Viral Niche Content / Affiliate Deal
    - Digital Resource / Template

    Return ONLY a valid JSON object:
    {
      "category": "Chosen Category",
      "project_title": "Project Name",
      "strategy": "Why this will generate clicks/revenue",
      "action_payload": "Specific requirements for the worker to build"
    }
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    decision = response.choices[0].message.content
    print("[ZACUX BRAIN DECISION]")
    print(decision)

if __name__ == "__main__":
    run_zacux_brain()
