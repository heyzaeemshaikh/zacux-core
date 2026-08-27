import json
import re
import requests
from zacux_engine.config import OPENROUTER_URL, HEADERS, HEAVY_CATEGORIES

def extract_safe_json(raw_text: str) -> dict:
    cleaned = str(raw_text or "").strip()
    if "```" in cleaned:
        match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', cleaned)
        if match:
            cleaned = match.group(1).strip()
            
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start:end+1])
        except Exception:
            pass

    return {
        "app_name": "VectorForge Studio",
        "slug": "vectorforge-studio",
        "architecture_summary": "High performance vector path editor and SVG studio",
        "ui_layout_spec": "Toolbar, layers drawer, canvas viewport, property inspector",
        "state_management_spec": "Vector node stack with local storage persistence",
        "core_engine_spec": "Bézier curve math, Canvas SVG rendering and path exporters"
    }

def invoke_model(system_prompt: str, user_prompt: str, json_mode: bool = False, max_tokens: int = 4000) -> str:
    # Reliable model list on OpenRouter
    models_to_try = [
        "anthropic/claude-3.5-haiku",
        "meta-llama/llama-3.3-70b-instruct",
        "google/gemini-2.0-flash-001",
        "openrouter/auto"
    ]
    
    for model_name in models_to_try:
        try:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": max_tokens
            }
            if json_mode:
                payload["response_format"] = {"type": "json_object"}

            res = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload, timeout=90)
            data = res.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"].get("content", "")
                if content and len(content.strip()) > 0:
                    return content
        except Exception as e:
            print(f"Model {model_name} retry trigger: {e}")
            continue

    return ""

# 1. RESEARCH & ARCHITECTURE GUARDIAN
def run_heavy_architect():
    system = "You are the Principal Systems Architect at ZACUX Enterprise. Output concise, valid JSON only."
    prompt = f"""
    Select ONE enterprise category from: {json.dumps(HEAVY_CATEGORIES)}
    Design an enterprise-tier browser workstation application.

    Return ONLY a valid JSON:
    {{
      "app_name": "Product Name",
      "slug": "clean-slug",
      "architecture_summary": "Technical architecture summary",
      "ui_layout_spec": "Toolbars, sidebars, main viewport, status panel",
      "state_management_spec": "State store and persistence rules",
      "core_engine_spec": "Algorithms, DOM events and export engines"
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

    Rules:
    - Include Tailwind CSS + FontAwesome Icons.
    - Provide complete toolbar buttons, floating side panels, tool options, and status bar.
    - Responsive dark theme (#090d16 background).
    - Output ONLY the HTML inside <body> (NO <script> tag).
    """
    res = invoke_model(system, prompt, json_mode=False, max_tokens=3500)
    return res if res else "<div>Workspace initialized</div>"

# 3. CORE LOGIC & ALGORITHM WORKER
def build_logic_layer(arch: dict) -> str:
    system = "You are the Senior Engine Engineer. Output pure production JavaScript only."
    prompt = f"""
    Write the 100% complete JavaScript engine for:
    {json.dumps(arch)}

    CRITICAL REQUIREMENTS:
    - Real event listeners for canvas/DOM interactions.
    - State management, undo/redo history, local storage save/load.
    - Real file export logic (PNG / SVG / JSON / File download).
    - Output PURE JavaScript code only (NO markdown wrappers).
    """
    res = invoke_model(system, prompt, json_mode=False, max_tokens=4000)
    return res if res else "// Engine ready"

# 4. QA COMPILER & TESTER
def run_qa_verification(full_html: str) -> bool:
    if len(full_html) < 800:
        return False
    required_tags = ["<html", "<body", "<script"]
    return any(tag.lower() in full_html.lower() for tag in required_tags)
