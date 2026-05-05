import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
from dotenv import load_dotenv

load_dotenv()

class Config:
    SF_USERNAME = os.getenv("SF_USERNAME")
    SF_PASSWORD = os.getenv("SF_PASSWORD")
    SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")
    SF_DOMAIN = os.getenv("SF_DOMAIN", "login")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = "llama-3.1-8b-instant"  # Groq's fast model
