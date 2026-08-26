import os
import json
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")

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
    
    candidate_models = [
        "llama-3.3-70b-versatile",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "gemma2-9b-it"
    ]
    
    last_error = None
    for model_name in candidate_models:
        try:
            print(f"[ATTEMPT] Trying model: {model_name}...")
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            print(f"[SUCCESS] Connected with model: {model_name}\n")
            print("[ZACUX BRAIN DECISION]")
            print(response.choices[0].message.content)
            return
        except Exception as e:
            print(f"[WARN] {model_name} failed: {e}")
            last_error = e

    print(f"[FATAL] All candidate models failed: {last_error}")
    exit(1)

if __name__ == "__main__":
    run_zacux_brain()
