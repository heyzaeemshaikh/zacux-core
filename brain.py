import os
import json
import requests

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

def try_openrouter():
    if not openrouter_key:
        print("[WARN] OpenRouter key missing.")
        return None
    
    print("[ATTEMPT] Connecting to OpenRouter Free Gateway...")
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "ZACUX Core"
    }
    
    # Models known to be free on OpenRouter
    models = [
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "openrouter/auto"
    ]
    
    for m in models:
        try:
            print(f"[TRY] OpenRouter Model: {m}")
            payload = {
                "model": m,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
            data = res.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                print(f"[FAIL] {m}: {data.get('error', {}).get('message', 'Unknown error')}")
        except Exception as e:
            print(f"[ERROR] {m}: {e}")
    return None

if __name__ == "__main__":
    decision = try_openrouter()
    if decision:
        print("\n=========================================")
        print("[ZACUX BRAIN AUTONOMOUS DECISION SUCCESS]")
        print("=========================================\n")
        print(decision)
    else:
        print("\n[FATAL] OpenRouter execution failed.")
        exit(1)
