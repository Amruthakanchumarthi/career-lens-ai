# 🚀 CareerLens AI: Intelligent Skill Gap & Upskilling Roadmap Generator

> An advanced prompt-engineered career intelligence tool that bridges the gap between candidate resumes and target job descriptions, delivering structured JSON roadmaps and actionable upskilling plans.

![Streamlit App Preview](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=for-the-badge&logo=streamlit)
![Groq API](https://img.shields.io/badge/Powered%20by-Groq%20LLM-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)

---

## 💡 The Problem & Solution
Traditional job searches and generic AI tools often provide vague career feedback (e.g., "learn more coding"). **CareerLens AI** solves this by enforcing strict prompt architecture and Chain-of-Thought reasoning to evaluate core competencies against specific industry requirements, rendering a hyper-targeted, week-by-week learning roadmap.

---

## 🛠️ Prompt Engineering Architecture
Unlike standard API wrappers, this project treats prompts as **software components**:
1. **Role & Persona Prompting:** Anchors the LLM as an elite 15+ year Senior Technical Recruiter and Career Coach.
2. **Chain-of-Thought (CoT) Constraints:** Forces the model to evaluate strengths, identify hard/soft gaps, and prioritize industry impact *before* generating output.
3. **Structured JSON Enforcement:** Utilizes system constraints and JSON-mode response formatting to guarantee predictable downstream data rendering.

---

## 📂 Project Structure
```text
career-lens-ai/
│
├── prompts/
│   └── system_prompt.txt   # Core system prompt & CoT instructions
├── app.py                  # Streamlit web application interface
├── main.py                 # Core CLI execution pipeline
├── requirements.txt        # Project dependencies
└── .gitignore              # Environment and cache exclusions