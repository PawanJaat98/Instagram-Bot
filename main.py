import requests
import time
import random
import os
from dotenv import load_dotenv
from instagrapi import Client
from datetime import datetime

load_dotenv()

# Instagram Credentials
INSTA_USERNAME = os.environ.get('INSTA_USER')
INSTA_PASSWORD = os.environ.get('INSTA_PW')

# Hugging Face API Configuration
API_TOKEN = os.environ.get('API_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Validate environment variables
if not all([INSTA_USERNAME, INSTA_PASSWORD]):
    raise ValueError("Missing required environment variables: INSTA_USER or INSTA_PW")

def generate_ai_image(prompt):
    """Generates an AI image using Hugging Face's SDXL model."""
    payload = {"inputs": prompt}
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            image_path = "generated_image.png"
            with open(image_path, "wb") as f:
                f.write(response.content)
            print("✅ Image saved as 'generated_image.png'")
            return image_path
        else:
            print("❌ Error:", response.json())
            return None
    except Exception as e:
        print(f"Generation failed: {e}")
        return None

def post_to_instagram(image_path, caption):
    """Posts the generated image to Instagram."""
    cl = Client()
    
    # Load session if available
    session_file = "session.json"
    if os.path.exists(session_file):
        cl.load_settings(session_file)

    try:
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)
        print("✅ Logged in successfully!")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return  # Stop execution if login fails
    cl.dump_settings(session_file)

    try:
        cl.photo_upload(image_path, caption=caption)
        print("✅ Image posted successfully!")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

    os.remove(image_path)

def get_random_prompt():
    """Generates a random AI art prompt."""
    themes = ["wheat farm", "futuristic city", "sunset landscape", "cyberpunk alley", "medieval castle"]
    styles = ["realistic", "cinematic lighting", "digital painting", "4K UHD"]
    return f"A {random.choice(themes)} with {random.choice(styles)}"

def main():
    """Main function to generate an image and post it to Instagram."""
    prompt = get_random_prompt()
    image_path = generate_ai_image(prompt)

    if image_path:
        caption = f"AI-generated art 🎨✨\nPrompt: {prompt}\n#AIArt #StableDiffusion #DailyAI"
        post_to_instagram(image_path, caption)
        print(f"✅ Posted at {datetime.now()}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
