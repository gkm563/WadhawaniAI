import google.generativeai as genai
from app.core.config import settings
import logging
import json
from typing import List, Dict, Any

logger = logging.getLogger("uvicorn.error")

# Configure Google Gemini client
gemini_available = False
api_key = settings.GEMINI_API_KEY

if api_key and "your-gemini" not in api_key:
    try:
        genai.configure(api_key=api_key)
        gemini_available = True
        logger.info("Google Gemini API client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to configure Google Gemini API: {str(e)}")
else:
    logger.warning("Gemini API key is unconfigured. Operating in mock simulation mode.")

def _call_gemini_json(prompt: str, system_instruction: str = "") -> dict:
    """
    Private helper to prompt Gemini 1.5 Flash and enforce JSON responses.
    """
    if not gemini_available:
        raise ValueError("Gemini is not configured")

    try:
        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=system_instruction
        )
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        if response and response.text:
            return json.loads(response.text)
        else:
            raise ValueError("Empty response received from Gemini API.")
    except Exception as e:
        logger.error(f"Gemini API invocation error: {str(e)}")
        raise e

def analyze_skill_gap(resume_text: str, target_role: str, experience_level: str) -> dict:
    """
    Compares the student's skills (extracted from resume) against the target job role's market requirements.
    Outputs gap score, matching skills, missing skills, and detailed actionable steps.
    """
    if not gemini_available or not resume_text.strip():
        # High-fidelity mock fallback to ensure robust offline/dry-run demo execution
        return {
            "gap_score": 55,
            "matching_skills": ["HTML", "CSS", "Basic Javascript", "Git"],
            "missing_skills": ["React.js", "State Management (Redux)", "TypeScript", "Tailwind CSS"],
            "recommendations": [
                {"skill": "React.js", "actionable_step": "Construct a dynamic Single Page Application (SPA) with routing."},
                {"skill": "TypeScript", "actionable_step": "Learn TypeScript basic types and type interfaces for props."},
                {"skill": "State Management (Redux)", "actionable_step": "Understand centralized states and implement basic context stores."}
            ]
        }

    system_instruction = (
        "You are an expert technical recruiter and career coach in India. Your goal is to analyze the student's "
        "skills extracted from their resume and compare them against target role requirements. "
        "You must output a strictly structured JSON response and strictly avoid hallucinations or fabrications. "
        "Always frame missing skills constructively. Under no circumstance should you include fake credentials."
    )

    prompt = f"""
    Please perform a skill gap analysis for a student targeting the role of '{target_role}' at '{experience_level}' experience level.
    
    Resume content:
    ---
    {resume_text}
    ---
    
    Analyze the skills found in the resume against standard market requirements for this target role.
    You must respond in JSON with EXACTLY this format:
    {{
        "gap_score": integer (between 0 and 100, where 100 means perfect match, 0 means complete gap),
        "matching_skills": ["skillA", "skillB", ...],
        "missing_skills": ["skillC", "skillD", ...],
        "recommendations": [
            {{
                "skill": "skillName",
                "actionable_step": "Constructive, realistic, low-cost study instructions to acquire this skill in India."
            }},
            ...
        ]
    }}
    """
    try:
        return _call_gemini_json(prompt, system_instruction)
    except Exception as e:
        logger.warning(f"Gemini skill-gap API failed. Falling back to mock generator: {str(e)}")
        # Default mock fallback return
        return {
            "gap_score": 60,
            "matching_skills": ["HTML Basics", "CSS Basics", "JS Basics"],
            "missing_skills": [f"{target_role} Advanced Stack", "Testing Frameworks", "Production Deployment"],
            "recommendations": [
                {"skill": f"{target_role} Advanced Stack", "actionable_step": "Explore core frameworks and libraries for this path."},
                {"skill": "Production Deployment", "actionable_step": "Learn how to build and host standard codebases using free cloud tools like Vercel or Render."}
            ]
        }

def generate_career_roadmap(target_role: str, missing_skills: List[str], duration_days: int, language: str = "en") -> dict:
    """
    Generates a localized 30/60-day career roadmap scheduled by weeks.
    Supports English or Hindi responses dynamically.
    """
    lang_instruction = "Respond in English." if language == "en" else "Respond in clean, friendly Hindi (using Devanagari script)."
    
    if not gemini_available:
        # High-fidelity mock localized roadmap response
        if language == "hi":
            return {
                "title": f"{duration_days} दिवसीय {target_role} करियर रोडमैप",
                "target_role": target_role,
                "duration_days": duration_days,
                "language": "hi",
                "milestones": [
                    {
                        "week": 1,
                        "title": "बुनियादी बातें सीखना (Getting Started)",
                        "tasks": ["वेब कैसे काम करता है समझें", "HTML और CSS संरचना का अभ्यास करें"],
                        "resources": ["MDN Web Docs हिंदी", "निःशुल्क Wadhwani ऑनलाइन मॉड्यूल"]
                    },
                    {
                        "week": 2,
                        "title": "मुख्य कौशल विकास (Core Skills)",
                        "tasks": ["जावास्क्रिप्ट फंक्शन्स और डोम मैनिपुलेशन सीखें", "एक साधारण प्रोजेक्ट बनाएं"],
                        "resources": ["फ्रीकोडकैंप हिंदी", "स्थानीय कॉलेज प्लेसमेंट सेल गाइड"]
                    }
                ]
            }
        else:
            return {
                "title": f"{duration_days}-Day {target_role} Skill Roadmap",
                "target_role": target_role,
                "duration_days": duration_days,
                "language": "en",
                "milestones": [
                    {
                        "week": 1,
                        "title": "Foundations & Environment setup",
                        "tasks": ["Set up local development tools", "Read core conceptual documentation"],
                        "resources": ["Free Interactive Tutorials", "MDN Reference Guides"]
                    },
                    {
                        "week": 2,
                        "title": "Interactive Projects",
                        "tasks": ["Build 2 small sandbox projects locally", "Push code repositories to GitHub"],
                        "resources": ["GitHub Guides", "Wadhwani Skilling Module 2"]
                    }
                ]
            }

    system_instruction = (
        f"You are an empathetic, expert skilling instructor in India. Your goal is to guide students on "
        f"how to acquire missing skills step-by-step. {lang_instruction} "
        "Ensure recommendations are low-bandwidth friendly, prioritize free resources, and emphasize practical milestones."
    )

    prompt = f"""
    Please generate a highly structured {duration_days}-day career roadmap for a student who wants to become a '{target_role}'.
    
    The student needs to acquire these missing skills:
    {", ".join(missing_skills)}
    
    Organize the roadmap by weeks (e.g. Week 1, Week 2, etc.) spanning the entire {duration_days} days.
    Make it highly actionable and include practical resources (preferring free Indian skilling portals and documentation).
    
    Return EXACTLY a JSON dictionary structured as follows:
    {{
        "title": "Roadmap title in the requested language",
        "target_role": "{target_role}",
        "duration_days": {duration_days},
        "language": "{language}",
        "milestones": [
            {{
                "week": 1,
                "title": "Week 1 milestone title (focused on a specific sub-topic or skill)",
                "tasks": [
                    "Task instruction 1",
                    "Task instruction 2"
                ],
                "resources": [
                    "Resource description 1 (e.g., Free Wadhwani skilling modules, standard documentation, YouTube)",
                    "Resource description 2"
                ]
            }},
            ...
        ]
    }}
    """
    try:
        return _call_gemini_json(prompt, system_instruction)
    except Exception as e:
        logger.warning(f"Roadmap Gemini generation failed. Using mock generator: {str(e)}")
        # Default safety return
        return {
            "title": f"PathPilot {duration_days}-Day Plan",
            "target_role": target_role,
            "duration_days": duration_days,
            "language": language,
            "milestones": [
                {
                    "week": 1,
                    "title": "Getting Started (शुरुआत करें)",
                    "tasks": ["Set up coding workspace", "Study core definitions"],
                    "resources": ["Official documentation", "Wadhwani Foundations Course"]
                }
            ]
        }

def evaluate_interview(role: str, questions: List[str], answers: List[str]) -> dict:
    """
    Evaluates a completed mock interview session.
    Assesses answer correctness, confidence level, and verbal communication capability.
    Generates a full scorecard and feedback details.
    """
    if not gemini_available:
        # High-fidelity mock assessment evaluation scorecard
        return {
            "overall_score": 75,
            "technical_score": 80,
            "communication_score": 70,
            "strengths": ["Demonstrates sound knowledge of fundamental concepts", "Structured thought process in explaining definitions"],
            "weaknesses": ["Lacks real-world deployment details in example structures", "Grammatical phrasing could be sharpened"],
            "detailed_feedback": [
                {
                    "question": q,
                    "user_answer": a if a else "[No answer provided]",
                    "feedback": "Solid answer. For enhancement, explain edge conditions or mention concrete projects where you utilized this concept.",
                    "model_answer": "A perfect response would describe the underlying architecture and present a clear deployment case."
                } for q, a in zip(questions, answers)
            ]
        }

    system_instruction = (
        "You are an expert HR and technical interviewer at a top technology firm in India. "
        "Your role is to evaluate student answers to a mock interview and provide detailed constructive feedback. "
        "Be extremely supportive but rigorous. Highlight positive achievements, point out clear technical gaps, "
        "and provide model answers to facilitate rapid learning. Respond strictly in JSON format."
    )

    q_a_block = ""
    for i, (q, a) in enumerate(zip(questions, answers)):
        q_a_block += f"Q{i+1}: {q}\nA{i+1}: {a}\n\n"

    prompt = f"""
    Please evaluate a mock interview completed by a student targeting the role of '{role}'.
    Here are the questions asked and the student's corresponding answers:
    
    {q_a_block}
    
    Provide a detailed evaluation scorecard. Rate technical quality and communication quality individually.
    You must output EXACTLY a JSON dictionary structured as follows:
    {{
        "overall_score": integer (between 0 and 100),
        "technical_score": integer (between 0 and 100),
        "communication_score": integer (between 0 and 100),
        "strengths": [
            "Strength point 1",
            "Strength point 2"
        ],
        "weaknesses": [
            "Area of improvement 1",
            "Area of improvement 2"
        ],
        "detailed_feedback": [
            {{
                "question": "Question text",
                "user_answer": "Student's raw answer",
                "feedback": "Individual question constructive assessment comments",
                "model_answer": "An ideal response for this question explaining the concept clearly."
            }},
            ...
        ]
    }}
    """
    try:
        return _call_gemini_json(prompt, system_instruction)
    except Exception as e:
        logger.warning(f"Gemini evaluation failed. Returning mock assessment: {str(e)}")
        return {
            "overall_score": 70,
            "technical_score": 72,
            "communication_score": 68,
            "strengths": ["Completed the practice mock test session", "Willingness to attempt all technical queries"],
            "weaknesses": ["Needs deeper conceptual clarity", "Answers should be more elaborate"],
            "detailed_feedback": [
                {
                    "question": q,
                    "user_answer": a if a else "[Empty response]",
                    "feedback": "This answer is basic. Spend more time studying key terminology.",
                    "model_answer": "Consult technical offline kits for comprehensive explanations."
                } for q, a in zip(questions, answers)
            ]
        }
