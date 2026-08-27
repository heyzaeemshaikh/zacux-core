def assemble_production_application(arch: dict, ui_html: str, js_engine: str) -> str:
    # Ensure safe strings (prevent NoneType crash)
    safe_ui = str(ui_html or "").strip()
    safe_js = str(js_engine or "").strip()

    clean_ui = safe_ui.replace("```html", "").replace("```", "").strip()
    clean_js = safe_js.replace("```javascript", "").replace("```js", "").replace("```", "").strip()

    # Fallback UI if agent returned empty
    if not clean_ui:
        clean_ui = f"""
        <div class="p-8 max-w-5xl mx-auto">
            <h1 class="text-2xl font-bold text-indigo-400">{arch.get('app_name', 'Enterprise Workspace')}</h1>
            <p class="text-slate-400 text-sm mt-1">{arch.get('architecture_summary', '')}</p>
            <div id="workspace-container" class="mt-6 panel-glass p-6 rounded-2xl min-h-[400px]"></div>
        </div>
        """

    full_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{arch.get('app_name', 'ZACUX Enterprise Tool')}</title>
  <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
  <link rel="stylesheet" href="[https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css)">
  <style>
    body {{ background-color: #090d16; color: #f1f5f9; font-family: system-ui, -apple-system, sans-serif; }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #0f172a; }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
    .panel-glass {{ background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }}
  </style>
</head>
<body class="min-h-screen flex flex-col overflow-x-hidden selection:bg-indigo-600 selection:text-white">

{clean_ui}

<script>
// ==================== ZACUX AUTONOMOUS SYNTHESIZED ENGINE ====================
{clean_js}
</script>
</body>
</html>
"""
    return full_page
