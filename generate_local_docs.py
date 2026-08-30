import os
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_presentation_html():
    ppt_md_path = os.path.join(ROOT_DIR, "ALOKA_PPT_CONTENT.md")
    if not os.path.exists(ppt_md_path):
        return

    with open(ppt_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    slides_raw = content.split("## Slide ")
    slides = []
    
    for s in slides_raw[1:]:
        lines = s.strip().split("\n")
        title_line = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        slides.append((title_line, body))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aloka Intelligence — Hackathon Presentation Deck</title>
  <style>
    :root {{
      --bg: #0B1017;
      --panel: #101722;
      --card: #141C28;
      --border: #263142;
      --primary: #2F5DA8;
      --primary-hover: #3A6DBD;
      --text: #F1F5F9;
      --text-muted: #94A3B8;
      --accent: #93B4E8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px 20px;
    }}
    .header {{
      max-width: 1000px;
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 25px;
      padding-bottom: 15px;
      border-bottom: 1px solid var(--border);
    }}
    .brand {{ display: flex; align-items: center; gap: 12px; }}
    .brand img {{ width: 38px; height: 38px; }}
    .brand h1 {{
      font-size: 16px;
      font-weight: 900;
      letter-spacing: 1px;
      text-transform: uppercase;
      font-family: monospace;
    }}
    .brand span {{
      font-size: 10px;
      color: var(--text-muted);
      letter-spacing: 2px;
      display: block;
    }}
    .deck-container {{
      max-width: 1000px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 25px;
    }}
    .slide-card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 35px 40px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
      page-break-after: always;
      position: relative;
    }}
    .slide-number {{
      font-family: monospace;
      font-size: 11px;
      font-weight: 700;
      color: var(--accent);
      background: #172640;
      border: 1px solid var(--border);
      padding: 4px 10px;
      border-radius: 6px;
      display: inline-block;
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    .slide-title {{
      font-size: 22px;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 10px;
      font-family: monospace;
    }}
    .slide-body h3 {{
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--accent);
      margin: 18px 0 8px 0;
      font-family: monospace;
    }}
    .slide-body ul {{ padding-left: 20px; margin-bottom: 15px; }}
    .slide-body li {{
      font-size: 14px;
      line-height: 1.6;
      color: #CBD5E1;
      margin-bottom: 6px;
    }}
    .speaker-note {{
      background: var(--card);
      border-left: 3px solid var(--primary);
      padding: 14px 18px;
      border-radius: 0 8px 8px 0;
      margin-top: 20px;
      font-style: italic;
      font-size: 13px;
      line-height: 1.6;
      color: #94A3B8;
    }}
    .speaker-note strong {{
      color: var(--text);
      font-style: normal;
      display: block;
      font-size: 11px;
      font-family: monospace;
      text-transform: uppercase;
      margin-bottom: 4px;
    }}
    .actions {{ margin-top: 30px; display: flex; gap: 12px; justify-content: center; }}
    .btn {{
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      text-decoration: none;
    }}
    .btn:hover {{ background: var(--primary-hover); }}
    @media print {{
      body {{ background: #fff; color: #000; padding: 0; }}
      .slide-card {{ background: #fff; border: 1px solid #ccc; color: #000; box-shadow: none; margin-bottom: 30px; }}
      .slide-title {{ color: #000; }}
      .slide-body li {{ color: #333; }}
      .speaker-note {{ background: #f4f4f4; color: #555; border-left-color: #333; }}
      .header, .actions {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="brand">
      <img src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" alt="KSP Emblem">
      <div>
        <h1>ALOKA INTELLIGENCE</h1>
        <span>STATE POLICE COMMAND CENTER — PRESENTATION DECK</span>
      </div>
    </div>
    <button class="btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
  </div>

  <div class="deck-container">
"""

    for idx, (title, body) in enumerate(slides):
        formatted_body = body
        formatted_body = re.sub(r'### (.*?)\n', r'<h3>\1</h3>', formatted_body)
        formatted_body = re.sub(r'^\* (.*?)$', r'<li>\1</li>', formatted_body, flags=re.MULTILINE)
        formatted_body = re.sub(r'((?:<li>.*?</li>\s*)+)', r'<ul>\1</ul>', formatted_body)
        formatted_body = re.sub(r'> (.*?)\n', r'<div class="speaker-note"><strong>🎤 Speaker Script</strong>\1</div>', formatted_body)
        formatted_body = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_body)

        html += f"""
    <div class="slide-card">
      <span class="slide-number">Slide {idx + 1} of {len(slides)}</span>
      <h2 class="slide-title">{title}</h2>
      <div class="slide-body">
        {formatted_body}
      </div>
    </div>
"""

    html += """
  </div>

  <div class="actions">
    <button class="btn" onclick="window.print()">Print or Export PDF Deck</button>
  </div>
</body>
</html>
"""

    out_path = os.path.join(ROOT_DIR, "ALOKA_PRESENTATION.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {out_path}")


def create_documentation_html():
    doc_md_path = os.path.join(ROOT_DIR, "ALOKA_PROJECT_DOCUMENTATION.md")
    if not os.path.exists(doc_md_path):
        return

    with open(doc_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Simple Markdown to HTML converter
    body_html = content
    # Code blocks
    body_html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', body_html, flags=re.DOTALL)
    # Headers
    body_html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', body_html, flags=re.MULTILINE)
    body_html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', body_html, flags=re.MULTILINE)
    body_html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', body_html, flags=re.MULTILINE)
    # Bold & Italic
    body_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', body_html)
    body_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', body_html)
    # Bullet points
    body_html = re.sub(r'^\* (.*?)$', r'<li>\1</li>', body_html, flags=re.MULTILINE)
    body_html = re.sub(r'((?:<li>.*?</li>\s*)+)', r'<ul>\1</ul>', body_html)
    # Blockquotes
    body_html = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', body_html, flags=re.MULTILINE)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aloka Intelligence — Master Technical Documentation</title>
  <style>
    :root {{
      --bg: #0B1017;
      --panel: #101722;
      --card: #141C28;
      --border: #263142;
      --primary: #2F5DA8;
      --text: #F1F5F9;
      --text-muted: #94A3B8;
      --accent: #93B4E8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
      padding: 40px 20px;
      display: flex;
      justify-content: center;
    }}
    .container {{
      max-width: 960px;
      width: 100%;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 50px 60px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 35px;
    }}
    .brand {{ display: flex; align-items: center; gap: 12px; }}
    .brand img {{ width: 44px; height: 44px; }}
    .brand h1 {{
      font-size: 20px;
      font-weight: 900;
      letter-spacing: 1px;
      text-transform: uppercase;
      font-family: monospace;
    }}
    h1 {{ font-size: 28px; margin: 30px 0 15px 0; color: #FFFFFF; font-family: monospace; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
    h2 {{ font-size: 20px; margin: 25px 0 12px 0; color: var(--accent); font-family: monospace; }}
    h3 {{ font-size: 15px; margin: 18px 0 8px 0; color: #FFFFFF; text-transform: uppercase; }}
    p {{ margin-bottom: 14px; color: #CBD5E1; font-size: 14px; }}
    ul {{ padding-left: 24px; margin-bottom: 16px; }}
    li {{ margin-bottom: 6px; color: #CBD5E1; font-size: 14px; }}
    pre {{
      background: #080C12;
      border: 1px solid var(--border);
      padding: 16px 20px;
      border-radius: 10px;
      overflow-x: auto;
      margin: 18px 0;
      font-family: monospace;
      font-size: 12px;
      color: #A7C4F2;
    }}
    blockquote {{
      border-left: 4px solid var(--primary);
      padding: 10px 16px;
      background: var(--card);
      color: var(--text-muted);
      margin: 15px 0;
      border-radius: 0 8px 8px 0;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 13px;
    }}
    th, td {{
      padding: 10px 14px;
      border: 1px solid var(--border);
      text-align: left;
    }}
    th {{
      background: #172640;
      color: #FFFFFF;
      font-family: monospace;
    }}
    td {{
      background: var(--card);
      color: #CBD5E1;
    }}
    .btn-print {{
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 12px;
      cursor: pointer;
    }}
    @media print {{
      body {{ background: #fff; color: #000; padding: 0; }}
      .container {{ background: #fff; border: none; box-shadow: none; padding: 20px; }}
      h1, h2, h3, p, li {{ color: #000 !important; }}
      pre {{ background: #f4f4f4; color: #000; border: 1px solid #ccc; }}
      td {{ background: #fff; color: #000; }}
      th {{ background: #eee; color: #000; }}
      .btn-print {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header-bar">
      <div class="brand">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" alt="KSP Emblem">
        <div>
          <h1>ALOKA INTELLIGENCE</h1>
          <p style="margin:0; font-size:11px; color:var(--text-muted);">MASTER TECHNICAL SPECIFICATION REPORT</p>
        </div>
      </div>
      <button class="btn-print" onclick="window.print()">🖨️ Print / Save PDF</button>
    </div>

    {body_html}
  </div>
</body>
</html>
"""

    out_path = os.path.join(ROOT_DIR, "ALOKA_DOCUMENTATION.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    create_presentation_html()
    create_documentation_html()
