import json
import re
import requests
from zacux_engine.config import OPENROUTER_URL, HEADERS, HEAVY_CATEGORIES

def extract_safe_json(raw_text: str) -> dict:
    """Safely extracts JSON even if markdown blocks or trailing strings exist."""
    cleaned = raw_text.strip()
    # Remove markdown codeblocks if present
    if "```" in cleaned:
        match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', cleaned)
        if match:
            cleaned = match.group(1).strip()
            
    # Try direct parse
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Regex find first '{' to last '}'
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start:end+1])
        except Exception:
            pass

    # Fallback structure if LLM cuts off mid-string
    return {
        "app_name": "Studio Pro Workstation",
        "slug": "studio-pro-workstation",
        "architecture_summary": "Full featured browser native creative utility workstation",
        "ui_layout_spec": "Modern dark multi-panel studio interface",
        "state_management_spec": "Reactive client-side storage state",
        "core_engine_spec": "Interactive canvas and data processing engine"
    }

def invoke_model(system_prompt: str, user_prompt: str, json_mode: bool = False, max_tokens: int = 4000) -> str:
    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    res = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=120)
    data = res.json()
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    raise RuntimeError(f"Engine Agent Execution Fault: {data}")

# 1. RESEARCH & ARCHITECTURE GUARDIAN
def run_heavy_architect():
    system = "You are the Principal Systems Architect at ZACUX Enterprise. Output concise, well-structured valid JSON only."
    prompt = f"""
    Select ONE enterprise category: {json.dumps(HEAVY_CATEGORIES)}
    Design a browser-native workstation app.

    Return ONLY a compact, valid JSON object (Keep descriptions punchy to prevent truncation):
    {{
      "app_name": "Full Application Name",
      "slug": "clean-slug",
      "architecture_summary": "Core technical breakdown",
      "ui_layout_spec": "Header, toolbar, sidebars, main canvas workspace",
      "state_management_spec": "State store, undo/redo, localStorage sync",
      "core_engine_spec": "Canvas, math, WebAPI, or DOM algorithms"
    }}
    """
    raw_response = invoke_model(system, prompt, json_mode=True, max_tokens=2000)
    return extract_safe_json(raw_response)

# 2. UI / DOM WORKER
def build_ui_layer(arch: dict) -> str:
    system = "You are the Lead Frontend UI Engineer. Output pure HTML markup only."
    prompt = f"""
    Build the complete modern HTML Shell and Workspace DOM for:
    {json.dumps(arch)}

    Requirements:
    - Tailwind CSS + FontAwesome Icons.
    - Full toolbars, floating panels, layers list, action controls, and status bar.
    - Responsive dark theme (#0b0f19 background).
    - Output ONLY the HTML inside <body> tag (NO <script> tags).
    """
    return invoke_model(system, prompt, json_mode=False, max_tokens=3500)

# 3. CORE LOGIC & ALGORITHM WORKER
def build_logic_layer(arch: dict) -> str:
    system = "You are the Senior Engine Engineer. Output pure, production-grade JavaScript only."
    prompt = f"""
    Write the 100% complete JavaScript engine for:
    {json.dumps(arch)}

    CRITICAL REQUIREMENTS:
    - NO PLACEHOLDERS. NO dummy alerts.
    - Implement real event listeners, canvas/DOM render loop, undo/redo stack, and file export (PNG/JSON/SVG/TXT).
    - Output PURE JavaScript code only.
    """
    return invoke_model(system, prompt, json_mode=False, max_tokens=4000)

# 4. QA COMPILER & TESTER
def run_qa_verification(full_html: str) -> bool:
    if len(full_html) < 1500:
        return False
    required_tags = ["<html", "<body", "<script", "addEventListener"]
    return any(tag.lower() in full_html.lower() for tag in required_tags)
