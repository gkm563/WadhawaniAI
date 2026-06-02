# PathPilot AI 🚀

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-blue?style=for-the-badge&logo=google-gemini)](https://deepmind.google/technologies/gemini/)
[![PWA](https://img.shields.io/badge/Features-Offline--Capable%20PWA-orange?style=for-the-badge&logo=progressive-web-apps)](https://web.dev/progressive-web-apps/)

> **Wadhwani AI + Google.org Hackathon MVP**  
> *Track: Higher Education & Skilling (Problem 3.2 — Job Readiness and Entrepreneurial Skills)*
> 
> Live Demo: [PathPilot AI on Vercel](https://wadhawani-ai.vercel.app) *(or your deployed Vercel URL)*

PathPilot AI is a mobile-first, low-bandwidth, and offline-capable skilling and employability assistant engineered specifically for underserved students, rural learners, and first-generation job seekers in Tier-2/Tier-3 colleges across India.

---

## 🌟 Key Features

1. **AI Skill Gap Analysis (Bilingual English / Hindi)**
   - Students upload a resume (PDF/TXT) or key-in skills manually.
   - Compares the student profile to target market roles, identifies matched skills vs gaps, and delivers actionable low-cost study recommendations.
2. **30-Day Personalized Career Roadmap**
   - Dynamic weekly timeline customized to address missing technical components.
   - Prioritizes free learning resources (MDN documentation, Wadhwani Skilling portals, etc.).
3. **Auditory Practice Interview Console**
   - Interactive voice/text mock session leveraging client-side Web Speech APIs (minimizes bandwidth).
   - Auditory synthesis: text-to-speech questions help visually impaired or slow-reading learners.
4. **Practice Scorecard Report**
   - Detailed grader measuring technical correctness and communication.
   - Strengths/weaknesses lists coupled with comparative question-by-question model answer sheets.
5. **Offline-First & Low-Connectivity PWA**
   - Built-in Service Worker caches core styles and layouts for instant local loading.
   - Auto-caches generated roadmaps and scorecards in client-side storage (`localStorage`/IndexedDB).
   - Offline toolkit pages serve pre-packaged study primer sheets even during absolute disconnects.

---

## 🛠 Production Architecture & Tech Stack

PathPilot AI is designed to scale and remain functional under poor network conditions:

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons, HTML5 PWA. Hosted on **Vercel** for instant edge rendering and static optimization.
- **Backend**: FastAPI (Python 3.10+), PyPDF2, Pydantic validations. Hosted on **Render** / Vercel Serverless.
- **Database**: Supabase (PostgreSQL + JWT Authentication).
- **AI Engine**: Google Gemini 1.5 Flash (via structured JSON output configuration).
- **Offline / Fallback Layer**: Integrated high-fidelity client-side simulators for all AI features. If the backend is unreachable or the user is offline, the app seamlessly runs full evaluations and roadmap generation completely in-browser without breaking.

---

## 📂 Project Structure

```text
/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── profiles.py     # User profiles CRUD
│   │   │   │   ├── skills.py       # Resume parsing & skill gap analysis
│   │   │   │   ├── roadmaps.py     # 30-day interactive timeline synthesis
│   │   │   │   └── interviews.py   # Interview session evaluation & scorecards
│   │   │   └── router.py           # Core APIRouter map
│   │   ├── core/
│   │   │   ├── config.py           # Environment settings loader
│   │   │   └── security.py         # Supabase JWT authentication helpers
│   │   ├── services/
│   │   │   ├── gemini.py           # Generative AI service (structured JSON)
│   │   │   ├── parser.py           # PyPDF2 plain-text resume extractor
│   │   │   └── supabase_client.py  # Supabase client connector
│   │   └── main.py                 # FastAPI application entrypoint
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Container configuration for Render
│
├── frontend/                 # Next.js 14 Progressive Web App
│   ├── public/
│   │   ├── manifest.json     # PWA metadata
│   │   └── sw.js             # Service Worker for offline asset caching
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx    # App shell, viewport, and Google Fonts
│   │   │   ├── page.tsx      # Unified Interactive Student Console Hub
│   │   │   └── offline/      # Offline study fallback packages
│   │   ├── lib/
│   │   │   └── translations.ts # English/Hindi localization dictionary
│   │   └── styles/
│   │       └── globals.css   # Theme styles & premium CSS transitions
│   ├── package.json          # Node dependencies
│   └── tailwind.config.js    # Styling design system
```

---

## ⚡ Quick Setup & Startup Guides

### 1. Backend Setup (FastAPI)

1. Navigate into the `/backend` folder:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your environment variables inside a `.env` file (copied from `.env.example`):
   ```env
   PORT=8000
   HOST=0.0.0.0
   ENVIRONMENT=development
   
   # Supabase Credentials (Optional)
   SUPABASE_URL=https://your-supabase-project.supabase.co
   SUPABASE_ANON_KEY=your-supabase-anon-key
   
   # Google Gemini AI API Configuration (Optional - falls back to simulator if missing)
   GEMINI_API_KEY=AIzaSy...
   GEMINI_MODEL=gemini-1.5-flash
   ```
4. Boot up the backend API server:
   ```bash
   python app/main.py
   ```
   *The FastAPI documentation is available at `http://localhost:8000/docs`.*

### 2. Frontend Setup (Next.js PWA)

1. Navigate into the `/frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure frontend environment variables in `.env.local`:
   ```env
   # API endpoint of the live or local FastAPI server
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Launch the development server:
   ```bash
   npm run dev
   ```
   *Open `http://localhost:3000` to interact with the PathPilot Console.*

---

## 🏁 Judge & Pitch Demo Walkthrough Guide

Use this sequence to present PathPilot AI during evaluations:

1. **Target Profile Setting**: Enter a student's name (e.g., Amit Kumar), choose **Frontend Developer (React.js)**, select **Entry Level**, and click **हिंदी में बदलें** to show instant English-to-Hindi interface translation.
2. **Employability Analysis**: Click **Upload Resume** (or enter manual skills). Click **Analyze Employability / रोजगार क्षमता का विश्लेषण करें**. The gauge dynamically fills to show a score (e.g., 48%), showcasing matching skills (green), missing skills (yellow), and actionable steps.
3. **Roadmap Generation**: Click **30-Day Roadmap / 30-दिवसीय रोडमैप**. A week-by-week interactive study curriculum loads showing checklists and links to free Wadhwani skilling modules.
4. **AI Practice Mock Session**: Scroll to the AI Practice Room and click **Start session / अभ्यास सत्र शुरू करें**. The AI greets the student with a synthesized audio question. Type the answer or speak into the microphone (transcribed locally using browser Web Speech APIs). Upon answering 3 questions, it generates an in-depth **Scorecard Report** showing overall, technical, and communication grades alongside strengths/weaknesses.
5. **Offline Mode Demonstration**: Toggle the network offline in Chrome Developer Tools. A dynamic **Offline mode warning** banner appears. The user can still interact, generate roadmaps, and practice mock interviews seamlessly using our robust client-side backup simulation layer!

---

## 🚀 Vercel Deployment Instructions

### Frontend (Next.js)
1. Push the repository to GitHub.
2. Go to Vercel, click **Add New Project**, and import the repository.
3. In the Root Directory settings, select `frontend` (or set the root directory of the project to `frontend`).
4. Add the Environment Variable `NEXT_PUBLIC_API_URL` pointing to your deployed live FastAPI URL (leave empty or set to `/` if using serverless rewrite configurations).
5. Click **Deploy**.
