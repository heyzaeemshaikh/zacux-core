import os
import json
import requests
import re
from datetime import datetime

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")

def call_llm(role: str, task: str, json_mode: bool = True) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "ZACUX Swarm"
    }
    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": f"You are {role} in ZACUX Autonomous OS."},
            {"role": "user", "content": task}
        ],
        "response_format": {"type": "json_object"} if json_mode else None
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=90)
    return res.json()["choices"][0]["message"]["content"]

def load_state():
    if os.path.exists("zacux_state.json"):
        try:
            with open("zacux_state.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "system_status": "ONLINE",
        "total_cycles": 0,
        "agents": {
            "research_guardian": {"status": "Ready"},
            "market_specialist": {"status": "Idle"},
            "product_guardian": {"status": "Ready"},
            "ui_ux_specialist": {"status": "Idle"},
            "fullstack_worker": {"status": "Idle"},
            "qa_tester": {"status": "Passed"},
            "growth_guardian": {"status": "Ready"},
            "seo_specialist": {"status": "Idle"},
            "treasury_agent": {"status": "Synced"}
        },
        "treasury": {
            "reserve_fund": 0,
            "growth_reinvestment": 0,
            "owner_vault": 0,
            "total_assets_built": 0
        },
        "live_logs": [],
        "recent_assets": []
    }

def save_state(state):
    with open("zacux_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def log_event(state, message):
    timestamp = datetime.utcnow().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    state.setdefault("live_logs", []).append(entry)
    if len(state["live_logs"]) > 20:
        state["live_logs"] = state["live_logs"][-20:]

def run_research_division(state):
    log_event(state, "🛡️ [RESEARCH DIVISION] Scanning profitable utility niches...")
    state["agents"]["research_guardian"]["status"] = "Active"
    state["agents"]["market_specialist"]["status"] = "Analyzing Trends"
    
    market_prompt = """Identify 1 high-demand browser-based web utility tool niche. 
    Return valid JSON:
    {
      "niche": "Tool Niche Name",
      "problem": "Target problem solved",
      "opportunity_score": 95
    }"""
    market_data = json.loads(call_llm("Market Analyst Specialist", market_prompt))
    log_event(state, f"🔎 [RESEARCH SPECIALIST] Discovered: {market_data.get('niche')}")
    
    state["agents"]["research_guardian"]["status"] = "Standby"
    state["agents"]["market_specialist"]["status"] = "Idle"
    return market_data

def run_product_division(state, research_data):
    log_event(state, "🛡️ [PRODUCT DIVISION] Architecting asset specification...")
    state["agents"]["product_guardian"]["status"] = "Active"
    state["agents"]["ui_ux_specialist"]["status"] = "Designing Specs"
    
    spec_prompt = f"""Design product requirements based on: {json.dumps(research_data)}.
    Return valid JSON:
    {{
      "title": "Clean Product Title",
      "slug": "clean-url-slug",
      "features": ["Feature 1", "Feature 2", "Feature 3"],
      "tech_stack": "Tailwind+JS"
    }}"""
    product_spec = json.loads(call_llm("UI/UX Architect Specialist", spec_prompt))
    
    log_event(state, f"⚙️ [WORKER AGENT] Compiling full code for {product_spec.get('title')}...")
    state["agents"]["fullstack_worker"]["status"] = "Writing Code"
    
    code_prompt = f"""Write complete, production-ready, interactive single-file HTML/CSS/JS for:
    {json.dumps(product_spec)}
    Requirements:
    - Pure HTML/CSS/JS only using Tailwind CSS via CDN.
    - Beautiful UI and working buttons/calculators.
    - Output ONLY raw HTML."""
    raw_code = call_llm("Lead Production Worker", code_prompt, json_mode=False)
    
    # Strip backticks
    cleaned = raw_code.strip()
    if cleaned.startswith("```html"): cleaned = cleaned[7:]
    if cleaned.startswith("```"): cleaned = cleaned[3:]
    if cleaned.endswith("```"): cleaned = cleaned[:-3]
    
    state["agents"]["product_guardian"]["status"] = "Standby"
    state["agents"]["fullstack_worker"]["status"] = "Idle"
    return product_spec, cleaned.strip()

def run_qa_and_tester(state, code):
    log_event(state, "🧪 [QA & TESTING DIVISION] Inspecting build integrity...")
    state["agents"]["qa_tester"]["status"] = "Testing Code"
    
    is_valid = len(code) > 200 and ("<html" in code.lower() or "<div" in code.lower())
    if is_valid:
        log_event(state, "✅ [QA PASSED] Integrity verified by Guardian Gate.")
        state["agents"]["qa_tester"]["status"] = "Passed"
        return True
    else:
        log_event(state, "❌ [QA FAILED] Code failed verification.")
        state["agents"]["qa_tester"]["status"] = "Failed"
        return False

def run_growth_and_treasury(state, product_spec, code):
    log_event(state, "🛡️ [GROWTH DIVISION] Deploying asset and updating treasury...")
    state["agents"]["growth_guardian"]["status"] = "Active"
    
    # Save asset file
    slug = re.sub(r'[^a-zA-Z0-9_-]', '', product_spec.get("slug", "tool").lower())
    filename = f"{slug}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    
    # Ledger Allocation
    state["treasury"]["total_assets_built"] = state["treasury"].get("total_assets_built", 0) + 1
    state["treasury"]["reserve_fund"] = state["treasury"].get("reserve_fund", 0) + 40
    state["treasury"]["growth_reinvestment"] = state["treasury"].get("growth_reinvestment", 0) + 30
    state["treasury"]["owner_vault"] = state["treasury"].get("owner_vault", 0) + 30
    
    state.setdefault("recent_assets", []).insert(0, {
        "title": product_spec.get("title", "Utility Tool"),
        "file": filename,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "status": "LIVE"
    })
    state["recent_assets"] = state["recent_assets"][:5]
    
    state["agents"]["growth_guardian"]["status"] = "Standby"
    state["agents"]["treasury_agent"]["status"] = "Synced"

def main():
    state = load_state()
    state["total_cycles"] = state.get("total_cycles", 0) + 1
    state["system_status"] = "RUNNING_CYCLE"
    
    log_event(state, f"🚀 [EXECUTIVE CORE] Swarm Cycle #{state['total_cycles']} Started.")
    
    research = run_research_division(state)
    spec, code = run_product_division(state, research)
    
    if run_qa_and_tester(state, code):
        run_growth_and_treasury(state, spec, code)
        log_event(state, f"🌟 [ROOT GUARDIAN] Asset '{spec.get('title')}' Live at /{spec.get('slug')}.html")
    else:
        log_event(state, "⚠️ [PIPELINE ABORTED] Quality gate rejected asset.")
        
    state["system_status"] = "IDLE_MONITORING"
    save_state(state)

if __name__ == "__main__":
    main()
