import requests
import time
import base64
import random
import os
import replicate
from dotenv import load_dotenv
from instagrapi import Client
from datetime import datetime

load_dotenv()

# Configuration
GENRE = "cyberpunk cityscape"  # Change your desired theme here
INSTA_USERNAME = os.environ.get('INSTA_USER')
INSTA_PASSWORD = os.environ.get('INSTA_PW')
REPLICATE_API_TOKEN = os.environ.get('REPLICATE_KEY')

# Replicate SDXL Model
REPLICATE_MODEL = "stability-ai/sdxl"

# Validate environment variables
if not all([INSTA_USERNAME, INSTA_PASSWORD, REPLICATE_API_TOKEN]):
    raise ValueError("Missing required environment variables: INSTA_USER, INSTA_PW, or REPLICATE_KEY")

def generate_ai_image(prompt):
    """Generates an AI image using Replicate's SDXL model."""
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
    
    try:
        output = replicate.run(
            REPLICATE_MODEL,
            input={
                "prompt": f"{prompt}, {GENRE}, 4K, trending on ArtStation",
                "width": 1024,
                "height": 1024
            }
        )

        if output:
            image_url = output[0]  # Replicate returns a URL
            return save_image(image_url)
    except Exception as e:
        print(f"Generation failed: {e}")
    
    return None

def save_image(image_url, filename="temp_post.jpg"):
    """Downloads image from Replicate URL and saves it locally."""
    img_data = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(img_data)
    return filename

def post_to_instagram(image_path, caption):
    cl = Client()
    
    # Load session if available
    session_file = "session.json"
    if os.path.exists(session_file):
        cl.load_settings(session_file)

    try:
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)
        print("Logged in successfully!")
    except Exception as e:
        print(f"Login failed: {e}")
        return  # Stop execution if login fails
    cl.dump_settings(session_file)

    try:
        cl.photo_upload(image_path, caption=caption)
        print("Image posted successfully!")
    except Exception as e:
        print(f"Upload failed: {e}")

    os.remove(image_path)

def get_random_prompt():
    themes = ["futuristic", "neon-lit", "rainy night", "hover vehicles", "digital utopia"]
    styles = ["unreal engine 5", "concept art", "cinematic lighting", "octane render"]
    return f"A {random.choice(themes)} {GENRE} with {random.choice(styles)}"

def main():
    prompt = get_random_prompt()
    image_path = generate_ai_image(prompt)
    if image_path:
        caption = f"AI-generated {GENRE} 🌆\nPrompt: {prompt}\n#{GENRE.replace(' ', '')} #AIart #DailyAI"
        post_to_instagram(image_path, caption)
        print(f"Posted at {datetime.now()}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
