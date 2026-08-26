import os
import json
import requests
from groq import Groq

groq_key = os.environ.get("GROQ_API_KEY")
openrouter_key = os.environ.get("OPENROUTER_API_KEY")

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

def try_groq():
    if not groq_key:
        return None
    print("[ATTEMPT] Connecting to Groq...")
    client = Groq(api_key=groq_key)
    
    # Active Groq models list
    active_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant"
    ]
    
    for m in active_models:
        try:
            print(f"[TRY] Model: {m}")
            res = client.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"[FAIL] {m}: {e}")
    return None

def try_openrouter():
    if not openrouter_key:
        return None
    print("[ATTEMPT] Falling back to OpenRouter...")
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        print(f"[FAIL] OpenRouter: {res.text}")
        return None

if __name__ == "__main__":
    decision = try_groq()
    if not decision:
        decision = try_openrouter()
        
    if decision:
        print("\n[ZACUX BRAIN SUCCESS]")
        print(decision)
    else:
        print("\n[FATAL] Both Groq and OpenRouter failed.")
        exit(1)
