import os
import subprocess
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

GMAIL_SENDER = os.getenv("GMAIL_SENDER_EMAIL")
GMAIL_RECEIVER = os.getenv("GMAIL_RECEIVER_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


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


def generate_newspaper_html(reader_name="Sudharshanam Buddha", edition_num="02"):
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    vol_str = f"VOL. I ... No. {edition_num}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>The Daily AI & ML Chronicle - Authentic Broadsheet Edition</title>
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

    /* Running Header for Pages 2+ */
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

    /* MASTHEAD (Page 1) */
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
      font-size: 26pt;
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

    /* COLUMNS & LAYOUTS */
    .columns-2 {{
      column-count: 2;
      column-gap: 18px;
      column-rule: 1px solid #e2e2e2;
      text-align: justify;
      hyphens: auto;
    }}

    .columns-3 {{
      column-count: 3;
      column-gap: 14px;
      column-rule: 1px solid #e5e5e5;
      text-align: justify;
      hyphens: auto;
    }}

    /* HEADLINES */
    .headline-main {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 19pt;
      font-weight: 900;
      line-height: 1.15;
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

    /* ARTICLE PARAGRAPHS */
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

    /* PULLQUOTE & CALLOUTS */
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

    /* TABLES */
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

    /* CODE SNIPPET SPAN */
    code {{
      font-family: 'Fira Code', monospace;
      font-size: 8.2pt;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
    }}

    /* BOTTOM INDEX / BANNER */
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

    /* FOOTER */
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
  <!-- PAGE 1: THE FRONT PAGE (LEAD NEWS & TITANS) -->
  <!-- ========================================== -->
  <div class="newspaper-page">
    <div>
      <!-- Masthead -->
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

      <!-- Lead Headline Banner -->
      <h2 class="headline-main">NVIDIA LEADERSHIP SHAKEUP & THE 50,000-CORE RUBIN REVOLUTION</h2>
      <div class="subdeck-main">Jensen Huang Steps Aside Amid Export Inquiries; Colette Kress Named Interim CEO as SC26 Supercomputing Rollout Shakes Silicon Valley</div>

      <!-- Page 1 Multi-Column Layout -->
      <div class="columns-2">
        <p class="no-indent dropcap">
          In an unprecedented realignment at the zenith of the global artificial intelligence boom, Nvidia Corporation confirmed a seismic executive restructuring alongside the debut of its next-generation computational architecture. Longtime President and Chief Executive Jensen Huang stepped down from his executive and board posts in mid-November following rigorous national security and export oversight inquiries into foreign intelligence vulnerabilities. Harvey C. Jones has assumed duties as the firm’s inaugural Independent Chairman, while veteran Chief Financial Officer Colette Kress ascends to Interim Chief Executive Officer.
        </p>

        <p>
          The boardroom transition arrives simultaneously with blistering financial performance. Nvidia reported fiscal third-quarter revenues of $115.8 billion—a 103 percent surge year-over-year—spearheaded by an unprecedented $107.6 billion contribution from its Data Center computational division. Despite early-stage scrutiny by the Securities and Exchange Commission concerning accounting procedures, Wall Street analysts noted that hyper-scaler infrastructure expenditure shows zero deceleration.
        </p>

        <div class="pullquote">
          “The transition from Blackwell to Rubin marks the end of simple cluster expansion and begins the era of unified heterogeneous silicon fabrics.”
        </div>

        <p>
          At the Supercomputing ’26 conference in Chicago, Nvidia countered market anxiety with the formal unveiling of <strong>Rubin HPC</strong>, an ultra-dense GPU purpose-built for scientific computing, physics simulations, and dense tensor operations. Packing more than 50,000 CUDA cores onto monolithic silicon interconnected via seventh-generation NVLink, volume shipments of Vera CPUs and Vera Rubin NVL72 liquid-cooled racks commenced this week across TSMC and Foxconn assembly pipelines.
        </p>

        <p>
          Crucially for local developers, Nvidia also introduced the <strong>DGX Spark Developer Kit</strong>. Utilizing native NVFP4 4-bit floating-point quantization, the desktop workstation allows AI practitioners to execute 120-billion-parameter Nemotron models locally without waiting in enterprise cloud queue lines.
        </p>

        <!-- Secondary Story -->
        <div style="border-top: 1.5px solid #222; padding-top: 8px; margin-top: 10px;">
          <span class="headline-kicker blue">BUILDER RADAR • SPATIAL AGENTS</span>
          <h3 class="headline-section" style="font-size: 11.5pt;">Barehands & The Death of Bulky Spatial Headsets</h3>
          <p class="no-indent">
            Developer Jared Rhodenizer’s open-source <code>barehands</code> initiative has taken developer communities by storm. Operating entirely on standard webcams with MediaPipe landmark tracking, it renders interactive 3D spatial glass cards and AI agent docks with zero hardware headsets or expensive sensory gloves. For practitioners developing camera-centric tools, it demonstrates the efficacy of fast client-side gesture recognition.
          </p>
        </div>
      </div>
    </div>

    <!-- Page 1 Bottom Index -->
    <div>
      <div class="frontpage-index">
        <div class="frontpage-index-item">
          <strong>Page 2 • The Curriculum</strong>
          The ML Taxonomy & The 3 Production Pitfalls (Géron Ch. 1)
        </div>
        <div class="frontpage-index-item">
          <strong>Page 3 • The Builder’s Lab</strong>
          Architecting Gallery Deduplication & Virtual Try-On
        </div>
        <div class="frontpage-index-item">
          <strong>Page 4 • Interview Sprint</strong>
          Mastering LangGraph StateGraphs & Human-in-the-Loop
        </div>
      </div>
      <div class="newspaper-footer">
        <div>THE DAILY AI & ML CHRONICLE • EDITION #01</div>
        <div>PAGE 1 OF 4</div>
      </div>
    </div>
  </div>


  <!-- ========================================== -->
  <!-- PAGE 2: MACHINE LEARNING FUNDAMENTALS (GÉRON) -->
  <!-- ========================================== -->
  <div class="newspaper-page">
    <div>
      <div class="running-header">
        <div>SECTION B • MACHINE LEARNING FOUNDATIONS</div>
        <div>CURATED FOR {reader_name.upper()} • GÉRON REVISION</div>
        <div>PAGE 2</div>
      </div>

      <span class="headline-kicker purple">CORE SYLLABUS REVISION • CHAPTER 1</span>
      <h2 class="headline-section" style="font-size: 16pt;">The Machine Learning Taxonomy & The Three Classic Failure Modes</h2>
      <div style="font-style: italic; font-size: 9pt; color: #555; margin-bottom: 10px;">
        Part I of our daily chapter-by-chapter mastery of Aurélien Géron’s "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow."
      </div>

      <div class="columns-2">
        <p class="no-indent dropcap">
          To build industrial-grade artificial intelligence systems, an engineer must first discard vague definitions and master the rigorous categorization of machine learning algorithms. In Chapter 1, Aurélien Géron classifies systems along three fundamental axes: the nature of human supervision during training, their ability to learn dynamically on the fly (batch vs. online), and how they generalize (instance-based vs. model-based).
        </p>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 8px 0 4px 0;">1. The Supervision Spectrum</h4>
        <p class="no-indent">
          <strong>Supervised Learning:</strong> The training dataset incorporates target labels (\(y\)). Algorithms learn a mapping function \(f(X) \to y\). Primary tasks comprise regression (predicting continuous target values) and classification (predicting discrete class memberships).
        </p>
        <p>
          <strong>Unsupervised Learning:</strong> The algorithm operates on unlabeled instances (\(X\)). The mathematical objective is to uncover underlying topology, latent manifolds, or probability densities without guidance. Core disciplines include:
        </p>
        <ul style="padding-left: 16px; margin: 0 0 8px 0; font-size: 9.2pt;">
          <li><em>Clustering:</em> Partitioning observations into cohorts (K-Means, DBSCAN, Hierarchical Clustering).</li>
          <li><em>Dimensionality Reduction:</em> Compressing feature dimensions while preserving maximum variance (Principal Component Analysis, t-SNE, UMAP).</li>
          <li><em>Anomaly Detection:</em> Modeling normal distributions to flag statistically improbable outliers (Isolation Forests, One-Class SVM).</li>
        </ul>
        <p>
          <strong>Self-Supervised & Metric Learning:</strong> A paradigm where the data generates its own pseudo-labels (e.g., masking words in Transformers or contrasting augmented image views in SimCLR). The resulting vector representations (embeddings) form the foundation of contemporary vector search.
        </p>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 12px 0 4px 0;">2. The Three Cardinal Production Pitfalls</h4>
        <p class="no-indent">
          When an algorithm fails in production, it invariably collapses into one of three structural categories:
        </p>

        <div class="editorial-box">
          <div class="editorial-box-title">Pitfall I: Overfitting (High Variance)</div>
          The model memorizes noise and idiosyncratic idiosyncrasies within the training set, achieving near-zero training error but catastrophic test loss.
          <br><strong>Remedies:</strong> Regularization (\(\ell_1, \ell_2\), Dropout), pruning trees, early stopping, and augmenting dataset volume.
        </div>

        <div class="editorial-box">
          <div class="editorial-box-title">Pitfall II: Underfitting (High Bias)</div>
          The model architecture lacks sufficient capacity or expressive power to capture the underlying reality of the data generating process.
          <br><strong>Remedies:</strong> Selecting a richer hypothesis class (e.g. polynomial features, deep neural layers) and relaxing regularization constraints.
        </div>

        <div class="editorial-box">
          <div class="editorial-box-title">Pitfall III: The "Data Mismatch" Trap</div>
          The most insidious pitfall in mobile and edge deployment. The model’s training distribution differs fundamentally from real-world user inference data (e.g., trained on clean web benchmarks, deployed on low-light smartphone cameras).
          <br><strong>Defense:</strong> Maintain a dedicated "train-dev" validation split sampled strictly from the training distribution to verify true generalization before deploying.
        </div>
      </div>

      <table class="newspaper-table">
        <thead>
          <tr>
            <th>Paradigm</th>
            <th>Primary Algorithms</th>
            <th>Supervision Type</th>
            <th>Canonical Production Use Case</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Supervised</strong></td>
            <td>Random Forest, XGBoost, ResNet</td>
            <td>Full Ground-Truth Labels (\(y\))</td>
            <td>Fraud detection, credit scoring, medical imaging</td>
          </tr>
          <tr>
            <td><strong>Unsupervised</strong></td>
            <td>DBSCAN, K-Means, PCA</td>
            <td>No Labels / Latent Structure</td>
            <td>Customer segmentation, visual duplicate clustering</td>
          </tr>
          <tr>
            <td><strong>Metric Learning</strong></td>
            <td>ArcFace, Siamese Nets, Triplet Loss</td>
            <td>Relative Distance / Similarity</td>
            <td>Face recognition, outfit matching, vector search</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="newspaper-footer">
      <div>NEXT EDITION: CHAPTER 2 — THE END-TO-END MACHINE LEARNING PROJECT PIPELINE</div>
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

      <span class="headline-kicker green">SYSTEMS DESIGN • APPLIED DEEP LEARNING</span>
      <h2 class="headline-section" style="font-size: 16pt;">Architectural Blueprints: Smart Gallery Cleaner & Affiliate Cashback Platform</h2>
      <div style="font-style: italic; font-size: 9pt; color: #555; margin-bottom: 10px;">
        Translating fundamental ML principles into production systems for your mobile and web applications.
      </div>

      <div class="columns-2">
        <h3 style="font-family: 'Playfair Display', serif; font-size: 12pt; border-bottom: 1px solid #111; padding-bottom: 3px; margin-bottom: 6px;">
          Blueprint 1: The Smart Gallery Cleaner
        </h3>
        <p class="no-indent">
          Cleaning gigabytes of user storage across images, high-resolution videos, and PDF receipts demands a multi-tiered filtering architecture to minimize client battery drain and compute latency:
        </p>

        <p>
          <strong>Tier 1 — Perceptual Hashing (Instant Local Filtering):</strong> Never run expensive neural networks on identical assets. Compute Difference Hash (<code>dHash</code>) or Average Hash (<code>aHash</code>) on downscaled 8x8 grayscale representations. Exact duplicates share a Hamming distance of zero (\(D_H = 0\)).
        </p>

        <p>
          <strong>Tier 2 — Self-Supervised Vision Embeddings:</strong> For near-duplicates (burst photos, slight angle changes, edited filters), pass images through an edge-quantized MobileNetV3 or CLIP visual encoder. Extract 512-dimensional vector representations and cluster them using Cosine Distance. If \(\cos(\theta) > 0.94\), group them into a single deletion card.
        </p>

        <p>
          <strong>Tier 3 — Video Keyframe Sampling & PDF OCR:</strong> For videos, extract I-frames at 1-second intervals using FFmpeg, compute frame hash trajectories, and detect static screenshots. For PDFs, extract embedded text streams directly via PDFMiner; fallback to Tesseract only on rasterized scans.
        </p>

        <h3 style="font-family: 'Playfair Display', serif; font-size: 12pt; border-bottom: 1px solid #111; padding-bottom: 3px; margin: 14px 0 6px 0;">
          Blueprint 2: Affiliate Cashback & Try-On Platform
        </h3>
        <p class="no-indent">
          An affiliate commerce engine combined with computer vision features requires strict separation between transactional guarantees and asynchronous inference:
        </p>

        <p>
          <strong>Virtual Try-On (VTON) Pipeline:</strong> Virtual apparel draping relies on high-resolution inpainting diffusion models (such as OOTDiffusion or CatVTON). The pipeline takes: (1) user pose landmarks via OpenPose/MediaPipe, (2) human body semantic parsing (segmenting clothing from skin), and (3) clothing image warping. Because diffusion inference requires 3–6 seconds, decouple the request via a Celery/Redis queue and notify the client via WebSockets.
        </p>

        <p>
          <strong>Face Recognition & Authentication:</strong> Implement an ArcFace backbone (Additive Angular Margin Loss). It maps facial features onto a hypersphere where angular separation corresponds to identity disparity. Enforce an anti-spoofing liveness check (blink detection or depth jitter) before authorizing cashback ledger transactions.
        </p>

        <p>
          <strong>Payment & Webhook Resilience:</strong> Ensure idempotent database transactions using unique transaction hash keys (UUIDv5) to prevent double payouts during network timeouts.
        </p>
      </div>

      <div class="editorial-box" style="margin-top: 14px;">
        <div class="editorial-box-title">Key Engineering Principle For Your Tech Stack</div>
        Always pair heavy Deep Learning microservices with a lightweight, rock-solid relational backend (PostgreSQL + FastAPI/Go). Let PostgreSQL handle ACID compliance for affiliate credits, while vector indexing (via pgvector or FAISS) powers instantaneous similarity lookups.
      </div>
    </div>

    <div class="newspaper-footer">
      <div>THE DAILY AI & ML CHRONICLE • SYSTEMS ENGINEERING</div>
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

      <span class="headline-kicker purple">INTERVIEW ACCELERATOR • AGENT ARCHITECTURES</span>
      <h2 class="headline-section" style="font-size: 16pt;">Demystifying LangGraph: Why Cyclic State Machines Rule Modern AI</h2>
      <div style="font-style: italic; font-size: 9pt; color: #555; margin-bottom: 10px;">
        Your daily technical homework to ace upcoming Senior AI Engineer and Agent Developer interviews.
      </div>

      <div class="columns-2">
        <p class="no-indent dropcap">
          In early 2024, most AI developers built systems using basic linear chains (Prompt \(\to\) Model \(\to\) Parser). Yet in real production environments, autonomous agents must iterate: they formulate a plan, execute a database tool, evaluate the result, detect an error, retry, and request human guidance. Standard LangChain DAGs (Directed Acyclic Graphs) cannot loop. Enter <strong>LangGraph</strong>.
        </p>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 8px 0 4px 0;">The Anatomy of a StateGraph</h4>
        <p class="no-indent">
          LangGraph models an agent as a state machine. It introduces three core primitives:
        </p>
        <ul style="padding-left: 16px; margin: 0 0 8px 0; font-size: 9.2pt;">
          <li><strong>The State Schema:</strong> A central typed dictionary (using Python’s <code>TypedDict</code> or Pydantic) that stores the cumulative memory—messages, tool execution records, and session metadata. Every node reads and updates this state.</li>
          <li><strong>Nodes (Workers):</strong> Independent Python functions or tool executors that accept the current state, perform a transformation, and return modified keys.</li>
          <li><strong>Edges (Routing Logic):</strong> Normal edges connect nodes unconditionally. Conditional edges inspect state attributes or tool calls and route execution dynamically (e.g. if model output contains <code>transfer_funds</code>, route to verification node; else route to end).</li>
        </ul>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 12px 0 4px 0;">Human-in-the-Loop Interrupts</h4>
        <p class="no-indent">
          In high-stakes financial operations—like sending payments in your cashback app—agents must never execute actions autonomously without user consent. LangGraph provides first-class <strong>persistence checkpointers</strong> (e.g. <code>SqliteSaver</code> or <code>PostgresSaver</code>) that pause the graph immediately before a designated node (<code>interrupt_before=["execute_payout"]</code>), save the exact execution state, and await human approval.
        </p>

        <div class="pullquote">
          “Chains run once and hope for the best. StateGraphs loop, self-correct, and persist until verified.”
        </div>

        <h4 style="font-family: 'Playfair Display', serif; font-size: 11pt; margin: 12px 0 4px 0;">Mock Interview Questions</h4>
        
        <div class="editorial-box">
          <div class="editorial-box-title">Q1: How do you prevent infinite loops in multi-agent routing?</div>
          <strong>Model Answer:</strong> "In LangGraph, we configure a strict <code>recursion_limit</code> parameter on the graph runner (defaulting to 25 steps). Furthermore, we encode loop counters directly inside the State schema. If an agent retries tool execution more than three times without progress, conditional edges forcefully route the execution to a human-escalation node."
        </div>

        <div class="editorial-box">
          <div class="editorial-box-title">Q2: When should you pick LangGraph over CrewAI or AutoGen?</div>
          <strong>Model Answer:</strong> "CrewAI is role-playing and chat-centric with fixed orchestration conventions. LangGraph is low-level, developer-first, and gives total deterministic control over state schemas, branch routing, and durable step-by-step persistence."
        </div>
      </div>

      <div style="border-top: 1.5px solid #111; margin-top: 10px; padding-top: 8px;">
        <span class="headline-kicker green">TONIGHT'S HOMEWORK</span>
        <p class="no-indent" style="font-size: 8.8pt;">
          Open your terminal, install <code>pip install -U langgraph langchain-core</code>, and implement a minimal 3-node cyclic graph: a Generator node that drafts text, an Evaluator node that scores it, and a Conditional Edge that loops back if score &lt; 8.
        </p>
      </div>
    </div>

    <!-- Page 4 Colophon -->
    <div>
      <div style="border-top: 1px solid #111; border-bottom: 1px solid #111; padding: 4px; text-align: center; font-size: 7.5pt; font-family: -apple-system, sans-serif; letter-spacing: 1px; text-transform: uppercase; background: #fafafa;">
        Printed and compiled automatically for {reader_name} • Tomorrow: End-to-End Pipeline & Feature Scaling
      </div>
      <div class="newspaper-footer">
        <div>THE DAILY AI & ML CHRONICLE • CONCLUSION OF EDITION #01</div>
        <div>PAGE 4 OF 4</div>
      </div>
    </div>
  </div>

</body>
</html>
"""
    return html


def build_and_send_newspaper_pdf(send_email=False, reader_name="Sudharshanam Buddha", edition_num="02"):
    date_slug = datetime.now().strftime("%Y_%m_%d")
    html_file = os.path.join(base_dir, "editions", f"edition_{date_slug}_newspaper.html")
    pdf_file = os.path.join(base_dir, "editions", f"The_Daily_AI_Chronicle_{date_slug}.pdf")

    # 1. Write HTML
    os.makedirs(os.path.join(base_dir, "editions"), exist_ok=True)
    html_content = generate_newspaper_html(reader_name=reader_name, edition_num=edition_num)
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
    msg["Subject"] = f"📰 The Daily AI & ML Chronicle — 4-Page Broadsheet PDF (Edition #01)"
    msg["From"] = GMAIL_SENDER
    msg["To"] = GMAIL_RECEIVER

    email_body = f"""Hello!

Here is your custom-formatted newspaper edition for today:
The Daily AI & ML Chronicle — Edition #01 (4-Page Broadsheet Edition)

Inside this PDF edition:
• Page 1: Front Page — Nvidia Leadership Transition & 50,000-Core Rubin GPU Launch
• Page 2: Machine Learning Foundations — Géron Book Ch. 1 Revision (Taxonomy & The 3 Pitfalls)
• Page 3: The Builder's Blueprint — Systems Design for Smart Gallery Cleaner & Affiliate Try-On
• Page 4: Career & Interview Accelerator — Mastering LangGraph StateGraphs & Practice Homework

Attached is your clean, high-resolution vector PDF formatted exactly like a classic 4-page broadsheet newspaper.
You can open it on your phone or laptop in any PDF reader.
"""
    msg.set_content(email_body)

    # Attach PDF
    with open(pdf_file, "rb") as f:
        pdf_data = f.read()
    msg.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=f"The_Daily_AI_Chronicle_Edition_{edition_num}.pdf"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_SENDER, GMAIL_PASSWORD)
        smtp.send_message(msg)

    print(f"Dispatched newspaper PDF to {GMAIL_RECEIVER}!")
    return pdf_file


if __name__ == "__main__":
    import sys
    should_send = "--send" in sys.argv or os.getenv("SEND_EMAIL", "0") == "1"
    build_and_send_newspaper_pdf(send_email=should_send, reader_name="Sudharshanam Buddha", edition_num="02")
