import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env")
    sys.exit(1)

genai.configure(api_key=api_key)

print(f"✅ Key found: {api_key[:5]}...")
print("\n🔍 Checking available models for this key...")

try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  👉 {m.name}")
            count += 1
    
    if count == 0:
        print("\n❌ No models found! Your API key might be invalid or has no access.")
    else:
        print(f"\n✅ Found {count} available models.")
        print("Use one of the names above in your logic.py file (remove the 'models/' prefix).")
        
except Exception as e:
    print(f"❌ Error contacting Google: {e}")