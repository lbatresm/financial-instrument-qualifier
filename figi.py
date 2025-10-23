from dotenv import load_dotenv
import os
import json
import urllib.request
import urllib.parse
import os


load_dotenv()
OPEN_FIGI_API_KEY = os.getenv("OPEN_FIGI_API_KEY")
OPENFIGI_BASE_URL = "https://api.openfigi.com"
