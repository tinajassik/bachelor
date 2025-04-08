from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

SKRAAFOTO_TOKEN = os.getenv("SKRAAFOTO_TOKEN")

if not SKRAAFOTO_TOKEN:
    print("⚠️ WARNING: SKRAAFOTO_TOKEN is not loaded")
