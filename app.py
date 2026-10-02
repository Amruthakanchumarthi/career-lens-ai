import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CareerLens AI - Skill Gap & Roadmap Generator",
    page_icon="🚀",
    layout="wide"
)

# Initialize Groq client
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def load_system_prompt():
    """Loads the system prompt from the prompts folder."""
    prompt_path = os.path.join("prompts", "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_pdf(pdf_file):
    """Extracts text content from an uploaded PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def analyze_resume(resume_text, job_description):
    """Sends the resume and JD to Groq using our prompt architecture."""
    if not client:
        return None, "API key missing. Please check your .env file."
        
    system_prompt = load_system_prompt()
    
    user_content = f"""
    Please analyze the following resume against the job description and return the output as valid JSON.

    ### TARGET JOB DESCRIPTION:
    {job_description}

    ### CANDIDATE RESUME:
    {resume_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content), None
    except Exception as e:
        return None, str(e)

# --- UI Layout ---
st.title("🚀 CareerLens AI")
st.markdown("### Intelligent Skill Gap & Upskilling Roadmap Generator")
st.write("Powered by advanced prompt engineering, Chain-of-Thought reasoning, and structured JSON outputs.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Target Job Description")
    jd_input = st.text_area("Paste the job description here...", height=300, placeholder="Looking for a Backend Engineer...")

with col2:
    st.subheader("📄 Candidate Resume")
    # Added option to upload a PDF or paste text
    upload_option = st.radio("Choose input method:", ["Upload Resume (PDF)", "Paste Text Summary"])
    
    resume_input = ""
    if upload_option == "Upload Resume (PDF)":
        uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])
        if uploaded_file is not None:
            resume_input = extract_text_from_pdf(uploaded_file)
            st.success("PDF successfully uploaded and read!")
    else:
        resume_input = st.text_area("Paste your resume text here...", height=200, placeholder="Software Engineer with 2 years experience...")

if st.button("Generate Upskilling Roadmap 🚀", type="primary"):
    if not jd_input or not resume_input:
        st.warning("Please provide both a job description and a resume (or PDF file) to analyze.")
    else:
        with st.spinner("Analyzing skill gaps and drafting your personalized roadmap..."):
            result, error = analyze_resume(resume_input, jd_input)
            
            if error:
                st.error(f"An error occurred: {error}")
            else:
                st.success("Analysis Complete!")
                
                # Display Match Score
                match_pct = result.get("match_percentage", 0)
                st.metric(label="Resume Match Score", value=f"{match_pct}%")
                
                # Core Strengths & Critical Gaps
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown("#### ✅ Core Strengths")
                    for strength in result.get("core_strengths", []):
                        st.markdown(f"- {strength}")
                
                with m_col2:
                    st.markdown("#### ⚠️ Critical Gaps")
                    for gap in result.get("critical_gaps", []):
                        st.markdown(f"- {gap}")
                
                # Roadmap Section
                st.markdown("---")
                st.markdown("### 🗺️ Week-by-Week Upskilling Roadmap")
                for week_item in result.get("upskilling_roadmap", []):
                    with st.expander(f"Week {week_item.get('week')}: {week_item.get('focus_area')}"):
                        st.markdown("**Actionable Tasks:**")
                        for task in week_item.get("actionable_tasks", []):
                            st.markdown(f"- {task}")
                        st.markdown("**Suggested Resources:**")
                        for resource in week_item.get("suggested_resources", []):
                            st.markdown(f"- {resource}")
                
                # Interview Tip & Download Report
                st.markdown("---")
                st.info(f"💡 **Recruiter Tip:** {result.get('interview_tip')}")
                
                # Download Button for JSON Roadmap
                json_string = json.dumps(result, indent=4)
                st.download_button(
                    label="📥 Download Roadmap as JSON",
                    data=json_string,
                    file_name="career_lens_roadmap.json",
                    mime="application/json"
                )