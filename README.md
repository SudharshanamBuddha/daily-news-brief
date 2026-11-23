# Daily AI & ML Chronicle

A personalized, automated, mobile-responsive daily newsletter system tailored for AI developments, hands-on ML fundamentals revision, and interview prep.

## Features
- **Mobile & Laptop Responsive**: Designed using responsive HTML email standards with clean typography and summary cards (approx. 2-min scan per article).
- **Sequential ML Fundamentals**: Follows Aurélien Géron's *Hands-On Machine Learning (3rd Edition)* chapter by chapter.
- **Tech Titans & Innovator Radar**: Tracks real-time industry moves (Nvidia, TSMC) and hands-on builders (Aishwarya Srinivasan, Barehands).
- **Interview & Project Tie-in**: Directly connects concepts to your upcoming projects (Gallery Cleaner deduplication, Virtual Try-on, Face Recognition, LangGraph StateGraphs).

## Project Structure
```
Daily_News_Brief/
├── .env                              # Gmail credentials (ignored by git)
├── .gitignore
├── profile.md                        # User preferences and learning tracker
├── send_edition.py                   # Edition compiler and email dispatcher
├── editions/                         # Local archive of daily editions (HTML)
└── .github/
    └── workflows/
        └── daily_brief.yml           # Cloud scheduled workflow (runs at 8:00 AM IST)
```

## Running When Your Laptop Is Off
Because a turned-off computer has no power to run local code, the project includes a **GitHub Actions** workflow:
1. Push this folder to a private GitHub repository.
2. In your repo settings, go to **Settings > Secrets and variables > Actions** and add:
   - `GMAIL_SENDER_EMAIL`
   - `GMAIL_RECEIVER_EMAIL`
   - `GMAIL_APP_PASSWORD`
3. The workflow runs every morning at **08:00 AM IST (02:30 UTC)** automatically from GitHub's cloud, sending the daily edition directly to your inbox so you can read it on your phone before even opening your laptop.
