import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import PyPDF2
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CareerLens AI - Skill Gap & Roadmap Generator",
    page_icon="🚀",
    layout="wide"
)

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
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

def generate_pdf_report(result):
    """Generates a downloadable PDF report from the analysis result safely."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)  # Explicit 15mm margins
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(180, 10, "CareerLens AI - Upskilling Roadmap", ln=True, align="C")
    pdf.ln(5)
    
    # Match Score
    match_pct = (
        result.get("match_percentage") 
        or result.get("match_score") 
        or result.get("percentage") 
        or 0
    )
    pdf.set_font("Arial", "B", 12)
    pdf.cell(180, 8, f"Resume Match Score: {match_pct}%", ln=True)
    pdf.ln(3)
    
    # Core Strengths
    pdf.set_font("Arial", "B", 11)
    pdf.cell(180, 6, "Core Strengths:", ln=True)
    pdf.set_font("Arial", "", 10)
    strengths = result.get("core_strengths") or result.get("strengths") or []
    for s in strengths:
        pdf.multi_cell(180, 5, f"- {s}")
    pdf.ln(3)
    
    # Critical Gaps
    pdf.set_font("Arial", "B", 11)
    pdf.cell(180, 6, "Critical Gaps:", ln=True)
    pdf.set_font("Arial", "", 10)
    gaps = result.get("critical_gaps") or result.get("gaps") or []
    for g in gaps:
        pdf.multi_cell(180, 5, f"- {g}")
    pdf.ln(3)
    
    # Roadmap
    pdf.set_font("Arial", "B", 11)
    pdf.cell(180, 6, "Week-by-Week Upskilling Roadmap:", ln=True)
    roadmap = result.get("upskilling_roadmap") or result.get("roadmap") or []
    for week_item in roadmap:
        w_num = week_item.get('week') or week_item.get('week_number') or "1"
        focus = week_item.get('focus_area') or week_item.get('focus') or "General"
        
        pdf.set_font("Arial", "B", 10)
        pdf.cell(180, 5, f"Week {w_num}: {focus}", ln=True)
        
        pdf.set_font("Arial", "", 9)
        pdf.multi_cell(180, 5, "Actionable Tasks:")
        for task in week_item.get("actionable_tasks", []) or week_item.get("tasks", []):
            pdf.multi_cell(180, 4, f"   * {task}")
            
        pdf.multi_cell(180, 5, "Suggested Resources:")
        for res in week_item.get("suggested_resources", []) or week_item.get("resources", []):
            pdf.multi_cell(180, 4, f"   * {res}")
        pdf.ln(3)
        
    # Recruiter Tip
    pdf.set_font("Arial", "B", 11)
    pdf.cell(180, 6, "Recruiter Tip:", ln=True)
    pdf.set_font("Arial", "", 10)
    tip = result.get("interview_tip") or result.get("tip") or "Highlight transferable skills."
    pdf.multi_cell(180, 5, tip)
    
    return pdf.output(dest='S').encode('latin1', errors='replace')

def analyze_resume(resume_text, job_description):
    """Sends the resume and JD to Groq using our prompt architecture."""
    if not client:
        return None, "Groq API key missing. Please check your environment variables."
        
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
    jd_input = st.text_area("Paste the job description here...", height=300, placeholder="Looking for an Engineer or Specialist...")

with col2:
    st.subheader("📄 Candidate Resume")
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
                
                # Display Match Score on UI
                match_pct = (
                    result.get("match_percentage") 
                    or result.get("match_score") 
                    or result.get("percentage") 
                    or 0
                )
                st.metric(label="Resume Match Score", value=f"{match_pct}%")
                
                strengths = (
                    result.get("core_strengths") 
                    or result.get("strengths") 
                    or result.get("key_strengths") 
                    or []
                )
                gaps = (
                    result.get("critical_gaps") 
                    or result.get("gaps") 
                    or result.get("missing_skills") 
                    or []
                )
                
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown("#### ✅ Core Strengths")
                    for strength in strengths:
                        st.markdown(f"- {strength}")
                
                with m_col2:
                    st.markdown("#### ⚠️ Critical Gaps")
                    for gap in gaps:
                        st.markdown(f"- {gap}")
                
                # Roadmap Section on UI
                roadmap = (
                    result.get("upskilling_roadmap") 
                    or result.get("roadmap") 
                    or result.get("learning_roadmap") 
                    or []
                )
                st.markdown("---")
                st.markdown("### 🗺️ Week-by-Week Upskilling Roadmap")
                for week_item in roadmap:
                    week_num = week_item.get('week') or week_item.get('week_number') or "1"
                    focus = week_item.get('focus_area') or week_item.get('focus') or "General Upskilling"
                    with st.expander(f"Week {week_num}: {focus}"):
                        st.markdown("**Actionable Tasks:**")
                        for task in week_item.get("actionable_tasks", []) or week_item.get("tasks", []):
                            st.markdown(f"- {task}")
                        st.markdown("**Suggested Resources:**")
                        for resource in week_item.get("suggested_resources", []) or week_item.get("resources", []):
                            st.markdown(f"- {resource}")
                
                # Interview Tip & PDF Download
                st.markdown("---")
                tip = (
                    result.get("interview_tip") 
                    or result.get("tip") 
                    or result.get("recruiter_tip") 
                    or "Focus on highlighting your transferable background during interviews."
                )
                st.info(f"💡 **Recruiter Tip:** {tip}")
                
                # Generate and offer PDF download button
                pdf_bytes = generate_pdf_report(result)
                st.download_button(
                    label="📥 Download Roadmap as PDF Report",
                    data=pdf_bytes,
                    file_name="career_lens_roadmap.pdf",
                    mime="application/pdf"
                )