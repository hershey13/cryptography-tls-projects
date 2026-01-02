import time
import google.generativeai as genai

# Replace with your actual API key
api_key = "AIzaSyCrSm8qEB4j6uwKjdgJo0oFNF7r_GFaMKA"

# Configure the API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

def generate_content(prompt):
    """Generates content using the Gemini API with retry logic."""
    retries = 3
    delay = 2  # seconds
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print("Max retries reached. Giving up.")
                return None

# Example usage:
prompt = "Write a short poem about the future."
response = generate_content(prompt)

if response:
    print(response)
