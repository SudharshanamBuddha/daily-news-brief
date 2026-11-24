import os
import sys
import subprocess
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
load_dotenv(os.path.join(base_dir, ".env"))

import news_engine

GMAIL_SENDER = os.getenv("GMAIL_SENDER_EMAIL")
GMAIL_RECEIVER = os.getenv("GMAIL_RECEIVER_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_browser_bin():
    # Windows Edge
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for p in edge_paths:
        if os.path.exists(p):
            return p
    # Linux / Mac fallbacks
    for name in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium"]:
        res = subprocess.run(["which", name], capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    return None


def generate_newspaper_html(reader_name="Sudharshanam Buddha"):
    curriculum = news_engine.get_current_curriculum()
    edition_num = curriculum["edition_num"]
    geron = curriculum["geron"]
    langgraph = curriculum["langgraph"]
    live_news = news_engine.fetch_live_news()
    
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    vol_str = f"VOL. I ... No. {edition_num}"

    # Pick lead news story from live feeds
    lead_story = live_news[0] if live_news else {
        "title": "Frontier AI Scaling & Next-Gen Open Models Accelerate",
        "summary": "AI labs continue rolling out quantized weights and decentralized inference fabrics enabling local desktop deployment.",
        "url": "https://huggingface.co/models",
        "source": "Industry Wire"
    }

    # If GEMINI_API_KEY is available, we synthesize enhanced editorial commentary
    lead_editorial = ""
    if GEMINI_API_KEY:
        try:
            prompt = (
                f"Write a 120-word concise, high-impact editorial broadsheet summary for an AI newspaper about this breakthrough: "
                f"Title: {lead_story['title']}. Summary: {lead_story['summary']}. "
                f"Focus on practical implications for machine learning engineers and developers. Plain text, professional, no hashtags."
            )
            ai_text = news_engine.call_gemini_writer(prompt, GEMINI_API_KEY)
            if ai_text:
                lead_editorial = ai_text.strip()
        except Exception as e:
            print(f"Gemini generation note: {e}")

    if not lead_editorial:
        lead_editorial = (
            f"{lead_story['summary']} Researchers and practitioners report significant advances in architectural "
            f"efficiency and open model accessibility, signaling continued momentum in applied edge intelligence."
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>The Sudharshanam Buddha Chronicle - Authentic Broadsheet Edition</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Playfair+Display:ital,wght@0,600;0,700;0,900;1,400;1,700&family=Lora:ital,wght@0,400;0,600;1,400&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4 portrait;
      margin: 12mm 14mm 14mm 14mm;
      @bottom-right {{
        content: counter(page);
      }}
    }}
    
    *, *:before, *:after {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    
    body {{
      margin: 0;
      padding: 0;
      background-color: #ffffff;
      color: #1a1a1a;
      font-family: 'Lora', Georgia, 'Times New Roman', serif;
      font-size: 9.8pt;
      line-height: 1.48;
    }}

    .newspaper-page {{
      width: 100%;
      min-height: 270mm;
      max-height: 272mm;
      overflow: hidden;
      page-break-after: always;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .newspaper-page:last-child {{
      page-break-after: avoid;
    }}

    .running-header {{
      display: flex;
      justify-content: space-between;
      border-bottom: 1.5px solid #1a1a1a;
      padding-bottom: 4px;
      margin-bottom: 12px;
      font-family: 'Cinzel', serif;
      font-size: 8pt;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #444;
    }}

    .masthead-wrapper {{
      text-align: center;
      margin-bottom: 10px;
    }}

    .ear-pieces {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #777;
      padding-bottom: 4px;
      margin-bottom: 6px;
      font-size: 7.5pt;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #555;
    }}

    .ear-subscriber {{
      font-weight: 700;
      color: #0f172a;
      background: #f1f5f9;
      padding: 2px 6px;
      border-radius: 3px;
    }}

    .masthead-title {{
      font-family: 'Cinzel', 'Playfair Display', serif;
      font-size: 24pt;
      font-weight: 900;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin: 2px 0 4px 0;
      color: #0d0d0d;
      line-height: 1.1;
    }}

    .masthead-subtitle {{
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 10pt;
      color: #333;
      margin-bottom: 6px;
    }}

    .date-bar {{
      display: flex;
      justify-content: space-between;
      border-top: 2.5px solid #111;
      border-bottom: 1px solid #111;
      padding: 4px 8px;
      font-size: 8pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      background: #fafafa;
    }}

    .columns-2 {{
      column-count: 2;
      column-gap: 18px;
      column-rule: 1px solid #e2e2e2;
      text-align: justify;
      hyphens: auto;
    }}

    .headline-main {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 18pt;
      font-weight: 900;
      line-height: 1.18;
      text-align: center;
      margin: 10px 0 6px 0;
      letter-spacing: -0.3px;
      color: #0a0a0a;
    }}

    .subdeck-main {{
      font-family: 'Lora', Georgia, serif;
      font-style: italic;
      font-size: 10pt;
      text-align: center;
      color: #444;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #ddd;
    }}

    .headline-section {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 14pt;
      font-weight: 700;
      line-height: 1.25;
      margin: 0 0 6px 0;
      color: #111;
    }}

    .headline-kicker {{
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 7.5pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: #c2410c;
      margin-bottom: 3px;
      display: block;
    }}

    .headline-kicker.blue {{ color: #1d4ed8; }}
    .headline-kicker.purple {{ color: #7e22ce; }}
    .headline-kicker.green {{ color: #15803d; }}

    p {{
      margin: 0 0 8px 0;
      text-indent: 14px;
    }}
    p.no-indent {{
      text-indent: 0;
    }}

    .dropcap::first-letter {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 38pt;
      float: left;
      line-height: 0.8;
      padding-top: 4px;
      padding-right: 8px;
      padding-bottom: 2px;
      color: #0d0d0d;
      font-weight: 900;
    }}

    .pullquote {{
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 11pt;
      line-height: 1.35;
      text-align: center;
      border-top: 1.5px solid #222;
      border-bottom: 1.5px solid #222;
      padding: 8px 14px;
      margin: 10px 0;
      color: #111;
      background: #fbfbfb;
    }}

    .editorial-box {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-left: 3.5px solid #1e293b;
      padding: 10px 12px;
      margin: 10px 0;
      font-size: 9pt;
      line-height: 1.4;
      break-inside: avoid;
    }}
    .editorial-box-title {{
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      font-weight: 700;
      font-size: 8pt;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #0f172a;
      margin-bottom: 4px;
    }}

    .newspaper-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0;
      font-size: 8.5pt;
      break-inside: avoid;
    }}
    .newspaper-table th {{
      border-top: 1.5px solid #222;
      border-bottom: 1.5px solid #222;
      padding: 5px 6px;
      font-family: -apple-system, sans-serif;
      font-size: 7.5pt;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      text-align: left;
      background: #f4f4f4;
    }}
    .newspaper-table td {{
      border-bottom: 1px solid #e0e0e0;
      padding: 5px 6px;
      vertical-align: top;
    }}

    code {{
      font-family: 'Fira Code', monospace;
      font-size: 8.2pt;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
    }}

    .frontpage-index {{
      border-top: 2px solid #111;
      border-bottom: 1.5px solid #111;
      padding: 6px 10px;
      margin-top: 8px;
      display: flex;
      justify-content: space-between;
      font-size: 8pt;
      background: #f9fafb;
    }}
    .frontpage-index-item {{
      flex: 1;
      padding: 0 8px;
      border-right: 1px solid #ddd;
    }}
    .frontpage-index-item:last-child {{
      border-right: none;
    }}
    .frontpage-index-item strong {{
      display: block;
      font-family: -apple-system, sans-serif;
      text-transform: uppercase;
      font-size: 7pt;
      letter-spacing: 0.5px;
      color: #64748b;
    }}

    .newspaper-footer {{
      border-top: 1px solid #999;
      padding-top: 4px;
      margin-top: 8px;
      display: flex;
      justify-content: space-between;
      font-size: 7.5pt;
      color: #666;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }}
  </style>
</head>
<body>

  <!-- ========================================== -->
  <!-- PAGE 1: THE FRONT PAGE (LEAD NEWS & PAPERS) -->
  <!-- ========================================== -->
  <div class="newspaper-page">
    <div>
      <div class="masthead-wrapper">
        <div class="ear-pieces">
          <div><span>🌐 EDITION: INTERNATIONAL</span> • <span>AI FRONTIER & APPLIED ML</span></div>
          <div class="ear-subscriber"><span>CURATED DAILY FOR {reader_name.upper()}</span></div>
        </div>
        <h1 class="masthead-title">The Sudharshanam Buddha Chronicle</h1>
        <div class="masthead-subtitle">A Private Broadsheet of Frontier Intelligence, Machine Learning Foundations & Systems Engineering</div>
        <div class="date-bar">
          <div>{vol_str}</div>
          <div>{date_str}</div>
          <div>DELIVERED TO YOUR PRIVATE INBOX</div>
        </div>
      </div>

      <h2 class="headline-main">{lead_story['title'].upper()}</h2>
      <div class="subdeck-main">Fresh Real-Time AI Developments Across Global Research Labs & Builder Communities</div>

      <div class="columns-2">
        <p class="no-indent dropcap">
          {lead_editorial}
        </p>

        <div class="pullquote">
          “Progress in modern machine learning moves from raw parameter scaling into verifiable agentic loops and efficient representations.”
        </div>

        <p>
          Today's highlighted development originates from recent community findings: <em>"{lead_story['title']}"</em>. 
          Engineers tracking autonomous agents and high-throughput systems note that architectural refinements continue to outpace simple hardware scaling.
        </p>

        <!-- Secondary Stories from Live Feeds -->
        <div style="border-top: 1.5px solid #222; padding-top: 8px; margin-top: 10px;">
          <span class="headline-kicker blue">COMMUNITY PAPERS & OPEN SOURCE</span>
          <h3 class="headline-section" style="font-size: 11pt;">
            {live_news[1]['title'] if len(live_news) > 1 else 'Next-Gen Open Representations'}
          </h3>
          <p class="no-indent" style="font-size: 9.2pt;">
            {live_news[1]['summary'] if len(live_news) > 1 else 'Explorations in contrastive pretraining continue to yield smaller, faster encoders suitable for client-side device deployments.'}
          </p>
        </div>
      </div>
    </div>

    <div>
      <div class="frontpage-index">
        <div class="frontpage-index-item">
          <strong>Page 2 • The Curriculum</strong>
          Ch. {geron['chapter']}: {geron['title']}
        </div>
        <div class="frontpage-index-item">
          <strong>Page 3 • The Builder’s Lab</strong>
          Architecting: {geron['project_tie']}
        </div>
        <div class="frontpage-index-item">
          <strong>Page 4 • Interview Sprint</strong>
          {langgraph['title']} & Mock Q&A
        </div>
      </div>
      <div class="newspaper-footer">
        <div>THE SUDHARSHANAM BUDDHA CHRONICLE • EDITION #{edition_num}</div>
        <div>PAGE 1 OF 4</div>
      </div>
    </div>
  </div>


  <!-- ========================================== -->
  <!-- PAGE 2: MACHINE LEARNING CURRICULUM (GÉRON) -->
  <!-- ========================================== -->
  <div class="newspaper-page">
    <div>
      <div class="running-header">
        <div>SECTION B • MACHINE LEARNING FOUNDATIONS</div>
        <div>CURATED FOR {reader_name.upper()} • GÉRON REVISION</div>
        <div>PAGE 2</div>
      </div>

      <span class="headline-kicker purple">SEQUENTIAL SYLLABUS REVISION • CHAPTER {geron['chapter']}</span>
      <h2 class="headline-section" style="font-size: 16pt;">{geron['title']}</h2>
      <div style="font-style: italic; font-size: 9pt; color: #555; margin-bottom: 10px;">
        Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd Edition) by Aurélien Géron
      </div>

      <div class="columns-2">
        <p class="no-indent dropcap">
          Mastering applied machine learning requires an exhaustive understanding of every layer of the modeling pipeline. In Chapter {geron['chapter']}, Aurélien Géron delves into: <strong>{geron['topics']}</strong>.
        </p>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 8px 0 4px 0;">Theoretical & Practical Mastery</h4>
        <p class="no-indent">
          When constructing industrial models, theoretical guarantees dictate production reliability. In this chapter's study:
        </p>
        <p>
          <strong>1. Core Algorithmic Mechanics:</strong> The relationship between mathematical loss functions and gradient stability determines convergence speed. For instance, understanding the trade-offs in metric selection ensures that training objectives mirror real business utility.
        </p>
        <p>
          <strong>2. Architectural Considerations:</strong> Preventing data leakage during preprocessing is vital. All transformations (mean imputation, standard scaling, and one-hot encoding) must be fitted strictly on the training partition, then transformed onto test sets via reproducible Scikit-Learn <code>Pipeline</code> objects.
        </p>

        <div class="editorial-box">
          <div class="editorial-box-title">Key Principle: Chapter {geron['chapter']} In Production</div>
          Always establish a clean, interpretable baseline before introducing deep neural architectures. An end-to-end pipeline with rigorous stratified cross-validation exposes data anomalies and label errors far earlier than raw model complexity.
        </div>
      </div>

      <table class="newspaper-table">
        <thead>
          <tr>
            <th>Module</th>
            <th>Primary Concept</th>
            <th>Production Risk</th>
            <th>Engineering Defense</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Pipeline Design</strong></td>
            <td>Transformers & Estimators</td>
            <td>Data Leakage</td>
            <td>Scikit-Learn Pipeline encapsulation</td>
          </tr>
          <tr>
            <td><strong>Metric Choice</strong></td>
            <td>Task-Specific Loss Formulation</td>
            <td>Metric-Goal Mismatch</td>
            <td>Stratified Validation Splits</td>
          </tr>
          <tr>
            <td><strong>Feature Scaling</strong></td>
            <td>Standardization vs Normalization</td>
            <td>Gradient Instability</td>
            <td>StandardScaler on non-outlier dense vectors</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="newspaper-footer">
      <div>NEXT EDITION: CHAPTER {geron['chapter'] + 1} OF GÉRON'S HANDS-ON ML</div>
      <div>PAGE 2 OF 4</div>
    </div>
  </div>


  <!-- ========================================== -->
  <!-- PAGE 3: THE BUILDER'S BLUEPRINT -->
  <!-- ========================================== -->
  <div class="newspaper-page">
    <div>
      <div class="running-header">
        <div>SECTION C • THE BUILDER'S BLUEPRINT</div>
        <div>PREPARED FOR {reader_name.upper()} • SYSTEMS DESIGN</div>
        <div>PAGE 3</div>
      </div>

      <span class="headline-kicker green">SYSTEMS DESIGN • APPLIED ENGINEERING</span>
      <h2 class="headline-section" style="font-size: 16pt;">Architectural Blueprint: {geron['project_tie']}</h2>
      <div style="font-style: italic; font-size: 9pt; color: #555; margin-bottom: 10px;">
        Translating fundamental ML principles into production systems for your mobile and web applications.
      </div>

      <div class="columns-2">
        <h3 style="font-family: 'Playfair Display', serif; font-size: 12pt; border-bottom: 1px solid #111; padding-bottom: 3px; margin-bottom: 6px;">
          Component Implementation Breakdown
        </h3>
        <p class="no-indent">
          Building high-performance client applications (such as the Smart Gallery Cleaner or the Affiliate Cashback engine) requires pairing mathematical elegance with strict resource budgets:
        </p>

        <p>
          <strong>Tier 1 — Fast Hash & Filter Layer:</strong> Never invoke heavy inference on raw assets. Use difference hashing (<code>dHash</code>) or perceptual hashing on downsampled 8x8 grayscale matrices. If Hamming distance \(D_H = 0\), immediately label as exact duplicates without consuming battery or GPU cycles.
        </p>

        <p>
          <strong>Tier 2 — Feature Embeddings:</strong> For visual assets that share stylistic or semantic similarity, run a lightweight edge encoder (MobileNetV3 or quantized CLIP). Extract 512-dimensional vectors and index them using FAISS or an in-memory cosine index.
        </p>

        <p>
          <strong>Tier 3 — Asynchronous Task Queue:</strong> Heavy operations (e.g. video keyframe parsing or diffusion virtual try-on draping) must be offloaded to asynchronous background workers (Celery/Redis) with WebSocket event notifications back to the user's mobile client.
        </p>

        <div class="editorial-box">
          <div class="editorial-box-title">System Architecture Rule</div>
          Decouple your transactional relational database (PostgreSQL for user profiles, affiliate ledger, and payouts) from your vector similarity services. Let the database enforce ACID compliance while the vector engine handles nearest-neighbor searches.
        </div>
      </div>
    </div>

    <div class="newspaper-footer">
      <div>THE SUDHARSHANAM BUDDHA CHRONICLE • SYSTEMS ENGINEERING</div>
      <div>PAGE 3 OF 4</div>
    </div>
  </div>


  <!-- ========================================== -->
  <!-- PAGE 4: INTERVIEW SPRINT (LANGGRAPH & AGENTS) -->
  <!-- ========================================== -->
  <div class="newspaper-page">
    <div>
      <div class="running-header">
        <div>SECTION D • CAREER & INTERVIEW ACCELERATOR</div>
        <div>PREPARED FOR {reader_name.upper()} • AGENTS & LANGGRAPH</div>
        <div>PAGE 4</div>
      </div>

      <span class="headline-kicker purple">INTERVIEW ACCELERATOR • {langgraph['title'].upper()}</span>
      <h2 class="headline-section" style="font-size: 16pt;">LangGraph Masterclass: {langgraph['title']}</h2>
      <div style="font-style: italic; font-size: 9pt; color: #555; margin-bottom: 10px;">
        Daily technical mastery for Senior AI Engineer and Agent Developer interview defense.
      </div>

      <div class="columns-2">
        <p class="no-indent dropcap">
          Production AI agent architectures must navigate uncertainty through cyclic loops, self-correction, and human-in-the-loop validation. Today's focus: <strong>{langgraph['concept']}</strong>.
        </p>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 8px 0 4px 0;">Technical Mechanics</h4>
        <p class="no-indent">
          In LangGraph, states are represented as typed schemas. When an agent invokes a tool or routes to another node, execution state is preserved across checkpoints, enabling durable retries and time-travel replay.
        </p>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 12px 0 4px 0;">Mock Interview Questions</h4>
        
        <div class="editorial-box">
          <div class="editorial-box-title">Q1: Technical Interview Defense</div>
          <strong>{langgraph['q1']}</strong>
        </div>

        <div class="editorial-box">
          <div class="editorial-box-title">Q2: System Architecture Defense</div>
          <strong>{langgraph['q2']}</strong>
        </div>
      </div>

      <div style="border-top: 1.5px solid #111; margin-top: 10px; padding-top: 8px;">
        <span class="headline-kicker green">TONIGHT'S HOMEWORK</span>
        <p class="no-indent" style="font-size: 8.8pt;">
          <strong>Action Task:</strong> {langgraph['homework']}
        </p>
      </div>
    </div>

    <div>
      <div style="border-top: 1px solid #111; border-bottom: 1px solid #111; padding: 4px; text-align: center; font-size: 7.5pt; font-family: -apple-system, sans-serif; letter-spacing: 1px; text-transform: uppercase; background: #fafafa;">
        Printed and compiled automatically for {reader_name} • Continuous Daily Learning Dispatch
      </div>
      <div class="newspaper-footer">
        <div>THE SUDHARSHANAM BUDDHA CHRONICLE • CONCLUSION OF EDITION #{edition_num}</div>
        <div>PAGE 4 OF 4</div>
      </div>
    </div>
  </div>

</body>
</html>
"""
    return html, edition_num


def build_and_send_newspaper_pdf(send_email=False, reader_name="Sudharshanam Buddha"):
    date_slug = datetime.now().strftime("%Y_%m_%d")
    html_content, edition_num = generate_newspaper_html(reader_name=reader_name)

    html_file = os.path.join(base_dir, "editions", f"edition_{date_slug}_newspaper.html")
    pdf_file = os.path.join(base_dir, "editions", f"The_Sudharshanam_Buddha_Chronicle_Edition_{edition_num}.pdf")

    # 1. Write HTML
    os.makedirs(os.path.join(base_dir, "editions"), exist_ok=True)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML source at: {html_file}")

    # 2. Render PDF using Edge Headless
    edge_bin = get_browser_bin()
    if not edge_bin:
        raise RuntimeError("No headless browser found to compile PDF!")

    cmd = [
        edge_bin,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Edge PDF generation failed: {res.stderr}")

    file_size_kb = os.path.getsize(pdf_file) / 1024
    print(f"Successfully rendered PDF newspaper: {pdf_file} ({file_size_kb:.1f} KB)")

    if not send_email:
        return pdf_file

    # 3. Email with PDF attachment
    if not GMAIL_SENDER or not GMAIL_PASSWORD or not GMAIL_RECEIVER:
        print("Gmail credentials missing. PDF generated locally.")
        return pdf_file

    msg = EmailMessage()
    msg["Subject"] = f"📰 The Sudharshanam Buddha Chronicle — Edition #{edition_num}"
    msg["From"] = GMAIL_SENDER
    msg["To"] = GMAIL_RECEIVER

    email_body = f"""Hello Sudharshanam!

Here is your custom-formatted newspaper edition for today:
The Sudharshanam Buddha Chronicle — Edition #{edition_num} (4-Page Broadsheet Edition)

Inside today's edition:
• Page 1: Front Page — Real-time AI developments & Hugging Face trending research
• Page 2: Machine Learning Foundations — Aurélien Géron Chapter Revision in order
• Page 3: The Builder's Blueprint — Systems Design for your upcoming projects
• Page 4: Career & Interview Accelerator — LangGraph daily topic & Mock Interview Q&A

Attached is your clean, high-resolution vector PDF broadsheet.
Enjoy your reading!
"""
    msg.set_content(email_body)

    # Attach PDF
    with open(pdf_file, "rb") as f:
        pdf_data = f.read()
    msg.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=f"The_Sudharshanam_Buddha_Chronicle_Edition_{edition_num}.pdf"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_SENDER, GMAIL_PASSWORD)
        smtp.send_message(msg)

    print(f"Dispatched newspaper PDF to {GMAIL_RECEIVER}!")
    return pdf_file


if __name__ == "__main__":
    should_send = "--send" in sys.argv or os.getenv("SEND_EMAIL", "0") == "1"
    build_and_send_newspaper_pdf(send_email=should_send, reader_name="Sudharshanam Buddha")
