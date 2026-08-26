import os
import json
import requests

openrouter_key = os.environ.get("OPENROUTER_API_KEY")

def call_ai(prompt: str, json_mode: bool = False) -> str:
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "ZACUX Core"
    }
    
    payload = {
        "model": "openrouter/auto",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"} if json_mode else None
    }
    
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=90)
    data = res.json()
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    raise RuntimeError(f"AI Call failed: {data}")

def run_zacux_workflow():
    # 1. BRAIN: Decide
    print("[1/2] BRAIN AGENT: Scanning opportunities...")
    brain_prompt = """
    You are the ZACUX Autonomous Brain.
    Decide on ONE high-converting single-page digital asset or web tool to build right now.
    Return ONLY a valid JSON:
    {
      "project_title": "Project Name",
      "category": "Web Tool or Digital Template",
      "strategy": "Why this sells/gets traffic",
      "specs": "Complete detailed requirements to build"
    }
    """
    decision_raw = call_ai(brain_prompt, json_mode=True)
    decision = json.loads(decision_raw)
    print(f"[DECISION] Building: {decision.get('project_title')}")

    # 2. WORKER: Build
    print("[2/2] WORKER AGENT: Generating complete functional asset...")
    worker_prompt = f"""
    You are the Senior Production Engineer at ZACUX Labs.
    Build a complete, responsive, single-file HTML page for:
    Title: {decision.get('project_title')}
    Specifications: {decision.get('specs')}

    Requirements:
    - Single self-contained HTML file with modern Tailwind CSS (via CDN) and interactive JavaScript.
    - Beautiful dark-mode UI, responsive cards, copy-to-clipboard buttons, and complete practical content.
    - Output ONLY pure HTML code. Do NOT wrap inside markdown backticks (no ```html).
    """
    asset_html = call_ai(worker_prompt, json_mode=False)
    
    # Strip markdown backticks if any
    cleaned = asset_html.strip()
    if cleaned.startswith("```html"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(cleaned)

    print("[SUCCESS] Production asset compiled and saved as index.html!")

if __name__ == "__main__":
    run_zacux_workflow()
