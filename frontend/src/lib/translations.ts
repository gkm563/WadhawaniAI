export type Language = "en" | "hi";

export const translations = {
  en: {
    // Brand Header
    brand: "PathPilot AI",
    tagline: "Your Career Navigator",
    offline_status: "Offline Mode Active (Static Caches Used)",
    online_status: "Connected",

    // Profile Settings
    profile_title: "Student Profile Setup",
    name_label: "Full Name",
    role_label: "Target Career Role",
    experience_label: "Experience Level",
    lang_toggle: "हिंदी में बदलें",
    save_btn: "Save Profile Settings",
    profile_saved: "Profile updated successfully!",

    // Skill Gap Analysis
    skills_title: "AI Skill Gap Analysis",
    upload_resume: "Upload Resume (PDF / TXT)",
    manual_skills: "Or Enter Skills Manually (comma separated)",
    analyzing: "Analyzing Skill Gaps...",
    analyze_btn: "Analyze Employability",
    matching_skills: "Skills you have",
    missing_skills: "Skills to learn",
    actionable_steps: "Actionable Learning Actions",
    gap_score_label: "Employability Readiness Score",

    // Career Roadmap
    roadmap_title: "Your 30-Day Personalized Roadmap",
    generate_roadmap_btn: "Synthesize 30-Day Roadmap",
    week_label: "Week",
    tasks_label: "Milestone Actions",
    resources_label: "Free Educational Materials",

    // Mock Interview Room
    interview_title: "Interactive AI Practice Room",
    start_interview_btn: "Initialize Mock Session",
    stop_interview_btn: "Stop Practice Run",
    text_placeholder: "Type your answer or speak using the microphone...",
    submit_response: "Send Response",
    next_question: "Proceeding to next query...",
    interview_complete: "Mock practice complete! Loading analysis scorecard...",
    mic_active: "Microphone listening... Speak now.",
    mic_inactive: "Click to speak (Speech-to-Text)",
    speech_not_supported: "Browser Speech-to-Text unsupported. Text mode active.",

    // Scorecard Evaluation
    evaluation_title: "Practice Scorecard Report",
    overall_score: "Overall Grade",
    tech_score: "Technical Score",
    comm_score: "Communication Score",
    strengths: "Strengths Identifiers",
    weaknesses: "Areas to Improve",
    detailed_feedback: "Detailed Answers Breakdown",
    question: "Question Asked",
    your_answer: "Your Answer Given",
    feedback: "Actionable Correction",
    model_answer: "Model Answer Guide",
    disclaimer: "All assessments are AI-generated based on practice responses. Consistently verify details."
  },
  hi: {
    // Brand Header
    brand: "पथपायलट AI",
    tagline: "आपका करियर मार्गदर्शक",
    offline_status: "ऑफ़लाइन मोड सक्रिय (स्थानीय डाटा)",
    online_status: "ऑनलाइन जुड़े हैं",

    // Profile Settings
    profile_title: "छात्र प्रोफ़ाइल सेटअप",
    name_label: "पूरा नाम",
    role_label: "लक्ष्य करियर पद",
    experience_label: "अनुभव का स्तर",
    lang_toggle: "Switch to English",
    save_btn: "प्रोफ़ाइल सुरक्षित करें",
    profile_saved: "प्रोफ़ाइल सफलतापूर्वक अपडेट हो गई!",

    // Skill Gap Analysis
    skills_title: "AI कौशल अंतर विश्लेषण",
    upload_resume: "रेज़्यूमे अपलोड करें (PDF / TXT)",
    manual_skills: "या कौशल मैन्युअल रूप से दर्ज करें (कोमा से अलग)",
    analyzing: "कौशल अंतर का विश्लेषण किया जा रहा है...",
    analyze_btn: "रोजगार क्षमता का विश्लेषण करें",
    matching_skills: "आपके पास जो कौशल हैं",
    missing_skills: "सीखने योग्य कौशल",
    actionable_steps: "सीखने के लिए व्यावहारिक कदम",
    gap_score_label: "रोजगार तैयारी स्कोर",

    // Career Roadmap
    roadmap_title: "आपका 30-दिवसीय व्यक्तिगत रोडमैप",
    generate_roadmap_btn: "30-दिवसीय रोडमैप तैयार करें",
    week_label: "सप्ताह",
    tasks_label: "महत्वपूर्ण कार्य",
    resources_label: "मुफ़्त शिक्षण सामग्री",

    // Mock Interview Room
    interview_title: "इंटरएक्टिव AI अभ्यास कक्ष",
    start_interview_btn: "अभ्यास सत्र शुरू करें",
    stop_interview_btn: "अभ्यास सत्र समाप्त करें",
    text_placeholder: "अपना उत्तर टाइप करें या माइक्रोफ़ोन का उपयोग करके बोलें...",
    submit_response: "उत्तर भेजें",
    next_question: "अगला प्रश्न लोड हो रहा है...",
    interview_complete: "अभ्यास पूरा हुआ! रिपोर्ट स्कोरकार्ड लोड किया जा रहा है...",
    mic_active: "माइक्रोफ़ोन चालू है... बोलें।",
    mic_inactive: "बोलने के लिए क्लिक करें (आवाज़ से टाइपिंग)",
    speech_not_supported: "ब्राउज़र में आवाज़ से टाइपिंग असमर्थ है। टेक्स्ट मोड चालू है।",

    // Scorecard Evaluation
    evaluation_title: "अभ्यास स्कोरकार्ड रिपोर्ट",
    overall_score: "कुल ग्रेड",
    tech_score: "तकनीकी स्कोर",
    comm_score: "संचार स्कोर",
    strengths: "आपकी ताकतें",
    weaknesses: "सुधार के क्षेत्र",
    detailed_feedback: "उत्तरों का विस्तृत विश्लेषण",
    question: "पूछा गया प्रश्न",
    your_answer: "आपका उत्तर",
    feedback: "व्यावहारिक सुझाव",
    model_answer: "आदर्श उत्तर मार्गदर्शिका",
    disclaimer: "सभी मूल्यांकन अभ्यास उत्तरों के आधार पर AI-जनरेटेड हैं। विवरण की पुष्टि स्वयं करें।"
  }
};
