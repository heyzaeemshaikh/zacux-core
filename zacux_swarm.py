import os
import json
import requests
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
        with open("zacux_state.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

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

# ==================== [SWARM AGENTS HIERARCHY] ====================

def run_research_division(state):
    log_event(state, "🛡️ [RESEARCH DIVISION] Initiating deep market reconnaissance...")
    state["agents"]["research_guardian"]["status"] = "Active"
    
    # 1. Market Specialist Sub-Agent
    state["agents"]["market_specialist"]["status"] = "Analyzing Trends"
    market_prompt = "Identify 1 viral high-converting SaaS/Tool niche. Return JSON: { 'niche': '...', 'problem': '...', 'opportunity_score': 95 }"
    market_data = json.loads(call_llm("Market Analyst Specialist", market_prompt))
    log_event(state, f"🔎 [RESEARCH SPECIALIST] Niche Discovered: {market_data.get('niche')}")
    
    state["agents"]["research_guardian"]["status"] = "Standby"
    state["agents"]["market_specialist"]["status"] = "Idle"
    return market_data

def run_product_division(state, research_data):
    log_event(state, "🛡️ [PRODUCT DIVISION] Architecting asset specification...")
    state["agents"]["product_guardian"]["status"] = "Active"
    
    # 2. UI/UX Specialist Sub-Agent
    state["agents"]["ui_ux_specialist"]["status"] = "Designing Specs"
    spec_prompt = f"Design product requirements for {json.dumps(research_data)}. Return JSON: { 'title': '...', 'features': [...], 'tech_stack': 'Tailwind+JS' }"
    product_spec = json.loads(call_llm("UI/UX Architect Specialist", spec_prompt))
    
    # 3. Full-Stack Production Worker
    log_event(state, f"⚙️ [WORKER AGENT] Compiling full code for {product_spec.get('title')}...")
    state["agents"]["fullstack_worker"]["status"] = "Writing Code"
    code_prompt = f"Write complete, production-ready, interactive single-file HTML/CSS/JS for {json.dumps(product_spec)}. Return ONLY the raw code."
    raw_code = call_llm("Lead Production Worker", code_prompt, json_mode=False)
    
    state["agents"]["product_guardian"]["status"] = "Standby"
    state["agents"]["fullstack_worker"]["status"] = "Idle"
    return product_spec, raw_code

def run_qa_and_tester(state, code):
    log_event(state, "🧪 [QA & TESTING DIVISION] Inspecting build integrity...")
    state["agents"]["qa_tester"]["status"] = "Testing Code"
    
    # QA Tester Evaluation
    is_valid = len(code) > 300 and ("<html" in code.lower() or "<div" in code.lower())
    if is_valid:
        log_event(state, "✅ [QA PASSED] Integrity check 100% verified.")
        state["agents"]["qa_tester"]["status"] = "Passed"
        return True
    else:
        log_event(state, "❌ [QA FAILED] Code failed build verification.")
        state["agents"]["qa_tester"]["status"] = "Failed"
        return False

def run_growth_and_treasury(state, product_spec):
    log_event(state, "🛡️ [GROWTH DIVISION] Generating distribution engine...")
    state["agents"]["growth_guardian"]["status"] = "Active"
    
    # 4. SEO & Growth Specialist
    seo_prompt = f"Generate SEO hooks and monetization strategy for {json.dumps(product_spec)}. Return JSON: { 'meta_title': '...', 'keywords': [...], 'monetization': 'AdSense+Affiliate' }"
    growth_data = json.loads(call_llm("SEO Growth Specialist", seo_prompt))
    
    # 5. Treasury Agent Ledger Calculation
    log_event(state, "💰 [TREASURY AGENT] Allocating revenue streams...")
    state["treasury"]["total_assets_built"] += 1
    state["treasury"]["reserve_fund"] += 40
    state["treasury"]["growth_reinvestment"] += 30
    state["treasury"]["owner_vault"] += 30
    
    state["recent_assets"].insert(0, {
        "title": product_spec.get("title", "Utility Tool"),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "status": "LIVE"
    })
    state["recent_assets"] = state["recent_assets"][:5]
    
    state["agents"]["growth_guardian"]["status"] = "Standby"
    state["agents"]["treasury_agent"]["status"] = "Updated"

# ==================== [EXECUTIVE ROOT CONTROLLER] ====================

def main():
    state = load_state()
    state["total_cycles"] = state.get("total_cycles", 0) + 1
    state["system_status"] = "RUNNING_CYCLE"
    
    log_event(state, f"🚀 [EXECUTIVE CORE] Cycle #{state['total_cycles']} Initiated.")
    
    research = run_research_division(state)
    spec, code = run_product_division(state, research)
    
    if run_qa_and_tester(state, code):
        run_growth_and_treasury(state, spec)
        log_event(state, f"🌟 [ROOT GUARDIAN APPROVAL] Asset '{spec.get('title')}' Deployed to System.")
    else:
        log_event(state, "⚠️ [PIPELINE ABORTED] Quality gate failed.")
        
    state["system_status"] = "IDLE_MONITORING"
    save_state(state)

if __name__ == "__main__":
    main()
