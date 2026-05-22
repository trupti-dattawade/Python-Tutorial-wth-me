import sys
import os
import groq 
import smtplib
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GROQ_MODEL=os.getenv("GROQ_MODEL")
SMTP_USERNAME=os.getenv("SMTP_USERNAME")
SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
SMTP_SENDER_EMAIL=os.getenv("SMTP_SENDER_EMAIL")
SMTP_SENDER_NAME=os.getenv("SMTP_SENDER_NAME")

if(GROQ_API_KEY is None or GROQ_MODEL is None or SMTP_USERNAME is None or SMTP_PASSWORD is None or SMTP_SENDER_EMAIL is None or SMTP_SENDER_NAME is None):
    print("Error: Missing environment variables. Please check your .env file.")
    sys.exit(1)
else:
    print("Environment variables loaded successfully.")  

