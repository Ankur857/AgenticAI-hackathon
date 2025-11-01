from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq chat model
model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    api_key=groq_api_key
)

# User inputs
inputs = {
    "name": "Ankur Verma",
    "skills": "React.js, Next.js, React Native, Python, and LangChain",
    "college": "KIET Group of Institutions, Ghaziabad",
    "projects": "Student Hub Universe — a collaborative student platform for learning and project sharing"
}

# Template
template = f"""
Dear Hiring Manager,

I am {inputs['name']}, currently pursuing my degree from {inputs['college']}. Over the past few years, I have developed strong skills in {inputs['skills']}, which have helped me grow both technically and professionally.

During my academic journey, I have worked on several projects, including {inputs['projects']}, which allowed me to apply my knowledge to real-world problems and strengthen my understanding of modern development practices.

I am particularly passionate about continuous learning and building efficient, user-focused solutions. I am confident that my technical expertise, combined with my enthusiasm for innovation, would make me a valuable addition to your team.

I would greatly appreciate the opportunity to discuss how my skills and experience align with your organization’s goals. Thank you for considering my application.

Sincerely,  
{inputs['name']}
"""

prompt = f"Refine and improve this cover letter for professionalism, tone, and impact and dont give key improvements and i should be normal english not too much high :\n\n{template}"

# Generate
response = model.invoke(prompt)

# Output
print("\n=== Final Generated Cover Letter ===\n")
print(response.content)

