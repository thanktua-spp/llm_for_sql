from dotenv import load_dotenv
import os

# Check if .env file exists
if os.path.exists('.env'):
    load_dotenv() 