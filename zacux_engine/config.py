import os

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com",
    "X-Title": "ZACUX Deep Engine"
}

# Heavy-Tier Production Categories (Full Complex Web Applications)
HEAVY_CATEGORIES = [
    "Full-Featured Vector Graphic / SVG Editor (Layers, Node Editing, Export)",
    "Interactive Audio Workstation / Synthesizer & Drum Machine (Web Audio API)",
    "Complete Markdown / Kanban Productivity Workspace (LocalStorage DB, Drag-and-Drop)",
    "Spreadsheet Engine with Formulas & Chart Visualizer (Formula Parser, Graphs)",
    "Client-Side Video & GIF Trimmer/Filter Studio (Canvas & WebCodecs)"
]
