import json
import requests
from zacux_engine.config import OPENROUTER_URL, HEADERS, HEAVY_CATEGORIES

def invoke_model(system_prompt: str, user_prompt: str, json_mode: bool = True, max_tokens: int = 4000) -> str:
    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"} if json_mode else None,
        "max_tokens": max_tokens
    }
    res = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=120)
    data = res.json()
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    raise RuntimeError(f"Engine Agent Execution Fault: {data}")

# 1. RESEARCH & ARCHITECTURE GUARDIAN
def run_heavy_architect():
    system = "You are the Principal Systems Architect at ZACUX Enterprise. You architect complex, production-grade browser applications."
    prompt = f"""
    Select ONE category from this enterprise list: {json.dumps(HEAVY_CATEGORIES)}
    Design a comprehensive, enterprise-tier web application architecture.
    
    Return ONLY a valid JSON:
    {{
      "app_name": "Full Application Name",
      "slug": "clean-url-slug",
      "architecture_summary": "Comprehensive breakdown of the engine",
      "ui_layout_spec": "Detailed specifications for Tailwind layout, toolbars, sidebars, modal views",
      "state_management_spec": "Data models, state variables, undo/redo stacks, persistence",
      "core_engine_spec": "Exact mathematical, canvas, DOM, or event listeners algorithms required"
    }}
    """
    return json.loads(invoke_model(system, prompt, json_mode=True))

# 2. UI / DOM WORKER
def build_ui_layer(arch: dict) -> str:
    system = "You are the Lead Frontend UI Engineer. You write comprehensive, pixel-perfect, dark-themed responsive DOM structures."
    prompt = f"""
    Build the complete HTML Shell, Header, Toolbar, Multi-Panel Workspace, Canvas/Main Area, and Status Bar for:
    {json.dumps(arch)}

    Rules:
    - Use Tailwind CSS and FontAwesome Icons via CDN.
    - Provide complete modal panels, dropdowns, keyboard shortcut hints, and full control panels.
    - Output ONLY the HTML inside the <body> tag (excluding <script> tags).
    """
    return invoke_model(system, prompt, json_mode=False, max_tokens=3500)

# 3. CORE LOGIC & ALGORITHM WORKER
def build_logic_layer(arch: dict) -> str:
    system = "You are the Senior Engine & Algorithms Engineer. You write deep, real-world, bug-free JavaScript execution logic."
    prompt = f"""
    Write the full production JavaScript engine for:
    {json.dumps(arch)}

    CRITICAL RULES:
    - NO PLACEHOLDERS. NO DUMMY ALERT(). NO '// implement later' comments.
    - Write full implementations: Event Listeners, State Machine, LocalStorage sync, File Import/Export, Rendering/Canvas loop, Undo/Redo.
    - Output pure JavaScript code only.
    """
    return invoke_model(system, prompt, json_mode=False, max_tokens=4000)

# 4. QA COMPILER & TESTER
def run_qa_verification(full_html: str) -> bool:
    if len(full_html) < 2000:
        return False
    required_tags = ["<html", "<body", "<script", "addEventListener", "localStorage"]
    return all(tag.lower() in full_html.lower() for tag in required_tags)

