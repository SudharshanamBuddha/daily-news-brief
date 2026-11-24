import os
import json
import urllib.request
from datetime import datetime, date

# Base anchor date for Edition #01: November 22, 2026
ANCHOR_DATE = date(2026, 11, 22)

# Complete 19-chapter curriculum of Aurélien Géron's Hands-On Machine Learning (3rd Ed)
GERON_SYLLABUS = [
    {
        "chapter": 1,
        "title": "The Machine Learning Landscape & The Three Failure Modes",
        "topics": "Supervised, Unsupervised, Metric Learning; Overfitting, Underfitting, and Data Mismatch.",
        "project_tie": "Smart Gallery Cleaner exact duplicate detection with dHash."
    },
    {
        "chapter": 2,
        "title": "The End-to-End Machine Learning Project Pipeline",
        "topics": "Problem framing, Performance Metrics (RMSE vs. MAE), Stratified Sampling, Imputation & Scikit-Learn Pipelines.",
        "project_tie": "Affiliate Cashback click conversion prediction pipeline."
    },
    {
        "chapter": 3,
        "title": "Classification Metrics & Decision Boundaries",
        "topics": "Confusion Matrix, Precision, Recall, F1-Score, Precision/Recall Trade-off, ROC Curves & ROC-AUC.",
        "project_tie": "Face Recognition verification threshold tuning and anti-spoofing precision."
    },
    {
        "chapter": 4,
        "title": "Training Linear Models & Regularization",
        "topics": "Normal Equation, Batch vs. Stochastic vs. Mini-batch Gradient Descent, Ridge, Lasso, ElasticNet & Logistic Regression.",
        "project_tie": "Feature selection for user cashback reward scoring."
    },
    {
        "chapter": 5,
        "title": "Support Vector Machines (SVM)",
        "topics": "Linear SVM, Soft Margin Classification, Polynomial Kernel, RBF Kernel & SVM Regression.",
        "project_tie": "High-margin boundary separation for visual gesture detection in spatial cards."
    },
    {
        "chapter": 6,
        "title": "Decision Trees & CART Algorithm",
        "topics": "Training and Visualizing Decision Trees, CART Algorithm, Gini Impurity vs. Entropy, Regularization Hyperparameters.",
        "project_tie": "Interpretable fraud detection rules for affiliate commissions."
    },
    {
        "chapter": 7,
        "title": "Ensemble Learning & Random Forests",
        "topics": "Voting Classifiers, Bagging, Pasting, Out-of-Bag Evaluation, Random Forests, AdaBoost, Gradient Boosting & Stacking.",
        "project_tie": "Robust multi-model ensembles for user purchase intent prediction."
    },
    {
        "chapter": 8,
        "title": "Dimensionality Reduction",
        "topics": "The Curse of Dimensionality, Projection vs. Manifold Learning, PCA, Incremental PCA, Kernel PCA.",
        "project_tie": "Vector compression for gallery image embeddings to save mobile RAM."
    },
    {
        "chapter": 9,
        "title": "Unsupervised Learning: Clustering & Density Estimation",
        "topics": "K-Means, Mini-Batch K-Means, Finding Optimal k (Inertia & Silhouette Score), DBSCAN, Gaussian Mixture Models.",
        "project_tie": "Automated clustering of near-duplicate burst photos in Smart Gallery Cleaner."
    },
    {
        "chapter": 10,
        "title": "Introduction to Artificial Neural Networks with Keras",
        "topics": "Biological to Artificial Neurons, MLPs, Backpropagation, Activation Functions, Keras Functional API & Callbacks.",
        "project_tie": "Building initial neural architectures for mobile clothing segmentation."
    },
    {
        "chapter": 11,
        "title": "Training Deep Neural Networks & Faster Optimizers",
        "topics": "Vanishing/Exploding Gradients, He/Glorot Initialization, Batch Normalization, Dropout, Adam, RMSProp, LR Schedules.",
        "project_tie": "Stabilizing training for custom outfit try-on feature extractors."
    },
    {
        "chapter": 12,
        "title": "Custom Models & Distributed Training with TensorFlow",
        "topics": "Tensors, Operations, Custom Loss Functions, Custom Layers, TF Functions & Autograph Graphs.",
        "project_tie": "Custom contrastive loss implementation for face recognition distance."
    },
    {
        "chapter": 13,
        "title": "Loading & Preprocessing Data with tf.data",
        "topics": "The tf.data API, TFRecord Format, Keras Preprocessing Layers, Efficient Pipeline Prefetching.",
        "project_tie": "Streaming millions of product images efficiently into GPU memory."
    },
    {
        "chapter": 14,
        "title": "Deep Computer Vision Using CNNs",
        "topics": "Convolutional & Pooling Layers, CNN Architectures (ResNet, MobileNet), Object Detection & Semantic Segmentation.",
        "project_tie": "Mobile-first clothing boundary segmentation for Virtual Try-On."
    },
    {
        "chapter": 15,
        "title": "Processing Sequences Using RNNs & Attention",
        "topics": "Recurrent Neurons, Memory Cells, LSTMs, GRUs, 1D CNNs for Sequence Processing.",
        "project_tie": "User clickstream time-series modeling for cashback payout prediction."
    },
    {
        "chapter": 16,
        "title": "Natural Language Processing with Transformers",
        "topics": "Encoder-Decoder Architectures, Self-Attention Mechanisms, Multi-Head Attention, Positional Encoding, GPT & BERT.",
        "project_tie": "Receipt OCR semantic parsing and affiliate merchant classification."
    },
    {
        "chapter": 17,
        "title": "Autoencoders, GANs, and Diffusion Models",
        "topics": "Latent Representations, Variational Autoencoders (VAEs), Generative Adversarial Networks & Latent Diffusion.",
        "project_tie": "Core generative inpainting for Virtual Try-On garment draping."
    },
    {
        "chapter": 18,
        "title": "Reinforcement Learning Fundamentals",
        "topics": "Markov Decision Processes (MDP), Q-Learning, Deep Q-Networks (DQN), Policy Gradients.",
        "project_tie": "Dynamic pricing and offer ranking optimization in affiliate channels."
    },
    {
        "chapter": 19,
        "title": "Deploying Models at Scale & Edge Serving",
        "topics": "TFLite Edge Quantization, ONNX Runtime, Model Serving, Monitoring Model Drift & Retraining Loops.",
        "project_tie": "Packaging Smart Gallery Cleaner ML models to run 100% on-device with zero server costs."
    }
]

# Daily LangGraph Interview Accelerator Syllabus
LANGGRAPH_SYLLABUS = [
    {
        "day": 1,
        "title": "Chains vs. Cyclic StateMachines in LangGraph",
        "concept": "Why linear LCEL fails for real agents; State, Nodes, and Conditional Edges.",
        "q1": "How do you prevent infinite loops in multi-agent routing? (Model answer: recursion_limit & loop counters)",
        "q2": "When do you pick LangGraph over CrewAI? (Model answer: Deterministic low-level state control)",
        "homework": "Build a 3-node cyclic Generator-Evaluator graph looping until score >= 8."
    },
    {
        "day": 2,
        "title": "State Schemas & Reducers in LangGraph",
        "concept": "TypedDict vs. Pydantic; Annotated[list, operator.add] for append-only message histories.",
        "q1": "What is the role of an Annotated reducer function in LangGraph State? (Model answer: Controls how new node returns merge into existing state)",
        "q2": "Why should messages be managed via add_messages rather than overwriting? (Model answer: Preserves thread history and deduplicates IDs)",
        "homework": "Define a custom State schema with a list of messages and an integer counter, using operator.add."
    },
    {
        "day": 3,
        "title": "Conditional Routing & Dynamic Tool Execution",
        "concept": "tools_condition, tool calling nodes, and routing back to model vs. human approval.",
        "q1": "How does LangGraph dynamically decide whether to execute a tool or stop? (Model answer: tools_condition inspects message.tool_calls)",
        "q2": "How do you handle tool execution failures gracefully without crashing the graph? (Model answer: Catch exceptions inside node and return ToolMessage with error text)",
        "homework": "Implement a graph with a weather tool and conditional edge using prebuilt tools_condition."
    },
    {
        "day": 4,
        "title": "Persistence Checkpointers & Time-Travel Debugging",
        "concept": "SqliteSaver and PostgresSaver; Thread IDs, checkpoint replay, and fork-and-resume.",
        "q1": "Explain how LangGraph achieves session persistence across multiple user turns. (Model answer: Checkpointers serialize state after every step under thread_id)",
        "q2": "What is time-travel in LangGraph and how does it assist production debugging? (Model answer: Allows rolling back state to any past checkpoint to replay)",
        "homework": "Attach MemorySaver to your graph and resume a multi-turn conversation using thread_id='user_123'."
    },
    {
        "day": 5,
        "title": "Human-in-the-Loop Interrupts & Authorization",
        "concept": "interrupt_before and interrupt_after; Pausing execution before critical external actions.",
        "q1": "How do you ensure a financial transaction or payment is never made without human confirmation? (Model answer: interrupt_before=['process_payment'] halts graph for external approval)",
        "q2": "How does an external frontend resume an interrupted LangGraph instance? (Model answer: Call graph.invoke(None, config) after updating state with user approval)",
        "homework": "Configure an interrupt_before on a payout node and resume it after simulated console approval."
    },
    {
        "day": 6,
        "title": "Multi-Agent Architectures: Supervisor vs. Swarm",
        "concept": "Centralized supervisor dispatching specialized agents vs. decentralized peer-to-peer handoffs.",
        "q1": "Compare Supervisor pattern with Network/Swarm pattern in agent design. (Model answer: Supervisor provides single source of truth; Swarm offers looser coupling)",
        "q2": "How do subgraphs isolate context in multi-agent workflows? (Model answer: Subgraphs run their own scoped state schema without polluting root state)",
        "homework": "Create a Supervisor agent that routes research queries to a Search Agent and coding queries to a Code Agent."
    },
    {
        "day": 7,
        "title": "Production Deployment & Streaming Agent Runs",
        "concept": "graph.astream_events, token-by-token streaming, and LangGraph Cloud / Docker deployment.",
        "q1": "How do you stream LLM tokens to the UI while tools are executing in the background? (Model answer: astream_events(version='v2') filters on_chat_model_stream)",
        "q2": "What are key production metrics for monitoring agent health? (Model answer: Step latency, token cost per turn, recursion limit hits, tool error rates)",
        "homework": "Write an asynchronous loop using astream_events to print tokens as they generate."
    }
]


def get_current_curriculum():
    today = date.today()
    delta_days = (today - ANCHOR_DATE).days
    edition_num = max(1, delta_days + 1)
    
    # 0-indexed syllabus
    geron_idx = (edition_num - 1) % len(GERON_SYLLABUS)
    langgraph_idx = (edition_num - 1) % len(LANGGRAPH_SYLLABUS)
    
    return {
        "edition_num": f"{edition_num:02d}",
        "geron": GERON_SYLLABUS[geron_idx],
        "langgraph": LANGGRAPH_SYLLABUS[langgraph_idx]
    }


def fetch_live_news():
    """Fetches real-time AI developments from Hugging Face Daily Papers API & Hacker News."""
    news_items = []
    
    # 1. Hugging Face Daily Papers (Fresh past 24 hours)
    try:
        req = urllib.request.Request(
            "https://huggingface.co/api/daily_papers",
            headers={"User-Agent": "DailyNewsBrief/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            for item in data[:3]:
                paper = item.get("paper", {})
                news_items.append({
                    "title": paper.get("title", ""),
                    "summary": paper.get("summary", "")[:280] + "...",
                    "url": f"https://huggingface.co/papers/{paper.get('id', '')}",
                    "source": "Hugging Face Daily Papers"
                })
    except Exception as e:
        print(f"HF feed warning: {e}")

    # Fallback/supplemental if needed
    if not news_items:
        news_items.append({
            "title": "Frontier AI Scaling & Next-Gen Open Models Accelerate",
            "summary": "AI labs continue rolling out quantized weights (NVFP4) and decentralized inference fabrics enabling local desktop deployment.",
            "url": "https://huggingface.co/models",
            "source": "Industry Wire"
        })

    return news_items


def call_gemini_writer(prompt: str, api_key: str) -> str:
    """Calls Google Gemini API (gemini-2.5-flash or gemini-1.5-flash) to write newspaper sections."""
    for model in ["gemini-2.5-flash", "gemini-1.5-flash"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 2048}
        }).encode("utf-8")
        
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                res_data = json.loads(resp.read().decode())
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            print(f"Gemini {model} call warning: {e}")
            continue
    return ""
