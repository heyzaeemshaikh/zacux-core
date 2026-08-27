import os
import json
import re
from datetime import datetime
from zacux_engine.agents import run_heavy_architect, build_ui_layer, build_logic_layer, run_qa_verification
from zacux_engine.synthesis import assemble_production_application

def load_state():
    if os.path.exists("zacux_state.json"):
        try:
            with open("zacux_state.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"system_status": "ONLINE", "total_cycles": 0, "live_logs": [], "recent_assets": []}

def save_state(state):
    with open("zacux_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def log(state, msg):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry)
    state.setdefault("live_logs", []).append(entry)
    if len(state["live_logs"]) > 25:
        state["live_logs"] = state["live_logs"][-25:]

def main():
    state = load_state()
    state["total_cycles"] = state.get("total_cycles", 0) + 1
    state["system_status"] = "SYNTHESIZING_HEAVY_APP"
    
    log(state, f"🚀 [HEAVY ENGINE] Commencing Deep Multi-Stage Synthesis Cycle #{state['total_cycles']}...")
    
    # Stage 1: Deep Architecture
    log(state, "📐 [STAGE 1: ARCHITECT] Designing enterprise application blueprint...")
    arch = run_heavy_architect()
    log(state, f"  >> Application Selected: {arch.get('app_name')}")

    # Stage 2: UI Layer
    log(state, "🎨 [STAGE 2: UI WORKER] Compiling multi-panel DOM layout...")
    ui_dom = build_ui_layer(arch)

    # Stage 3: Logic Engine
    log(state, "⚙️ [STAGE 3: LOGIC WORKER] Coding full algorithmic JS engine...")
    js_engine = build_logic_layer(arch)

    # Stage 4: Synthesis & QA Verification
    log(state, "🧪 [STAGE 4: SYNTHESIZER] Merging layers and running QA Gate...")
    compiled_app = assemble_production_application(arch, ui_dom, js_engine)
    
    if run_qa_verification(compiled_app):
        slug = re.sub(r'[^a-zA-Z0-9_-]', '', arch.get("slug", "heavy-app").lower())
        filename = f"{slug}.html"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(compiled_app)
            
        log(state, f"✅ [QA VERIFIED] Production asset '{arch.get('app_name')}' deployed ({len(compiled_app)} bytes).")
        
        # State Update
        state.setdefault("treasury", {})
        state["treasury"]["total_assets_built"] = state["treasury"].get("total_assets_built", 0) + 1
        state["treasury"]["owner_vault"] = state["treasury"].get("owner_vault", 0) + 120
        state["treasury"]["growth_reinvestment"] = state["treasury"].get("growth_reinvestment", 0) + 120
        state["treasury"]["reserve_fund"] = state["treasury"].get("reserve_fund", 0) + 160
        
        state.setdefault("recent_assets", []).insert(0, {
            "title": arch.get("app_name"),
            "file": filename,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            "status": "LIVE"
        })
        state["recent_assets"] = state["recent_assets"][:6]
    else:
        log(state, "❌ [QA GATE REJECTED] Synthesized codebase did not meet strict density threshold.")

    state["system_status"] = "IDLE_MONITORING"
    save_state(state)

if __name__ == "__main__":
    main()
