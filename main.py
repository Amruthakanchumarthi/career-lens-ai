import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_system_prompt():
    """Loads the system prompt from the prompts folder."""
    prompt_path = os.path.join("prompts", "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_resume(resume_text, job_description):
    """Sends the resume and JD to Groq using our prompt architecture."""
    system_prompt = load_system_prompt()
    
    user_content = f"""
    ### TARGET JOB DESCRIPTION:
    {job_description}

    ### CANDIDATE RESUME:
    {resume_text}
    """

    print("🤖 Analyzing resume against job description via Groq...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # High-performance free model on Groq
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        response_format={"type": "json_object"}, # Forces JSON output
        temperature=0.2
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    sample_resume = "Software Engineer with 2 years of experience in Python, Flask, and basic SQL. Built REST APIs and managed local databases."
    sample_job_description = "Looking for a Backend Engineer with 3+ years experience, expert Python, FastAPI, Docker, AWS, and CI/CD pipelines."

    result_json = analyze_resume(sample_resume, sample_job_description)
    
    print("\n📊 Upskilling Roadmap Result:")
    print(result_json)