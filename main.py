import requests
import time
import base64
import random
import os
from dotenv import load_dotenv
from instagrapi import Client
from datetime import datetime
load_dotenv()
# Configuration
GENRE = "cyberpunk cityscape"  # Change your desired theme here
INSTA_USERNAME = os.environ.get('INSTA_USER')
INSTA_PASSWORD = os.environ.get('INSTA_PW')
STABILITY_KEY = os.environ.get('STABILITY_KEY')

# Stability.ai API endpoint
# Switch to SDXL 1.0 (free tier compatible)
STABILITY_API = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

# Validate environment variables
if not all([INSTA_USERNAME, INSTA_PASSWORD, STABILITY_KEY]):
    raise ValueError("Missing required environment variables: INSTA_USER, INSTA_PW, or STABILITY_KEY")

# def generate_ai_image(prompt):
#     headers = {
#         "Authorization": f"Bearer {STABILITY_KEY}",
#         "Accept": "application/json",
       
       
#     }
    
#     # Correct JSON payload format
#     form_data = {
#         "prompt": (None, f"{prompt}, {GENRE}, 4k, trending on ArtStation"),
#         "height": (None, "1024"),
#         "width": (None, "1024"),
#         "cfg_scale": (None, "7"),
#         "steps": (None, "30"),
#         "output_format": (None, "png")
#     }

#     response = requests.post(STABILITY_API, headers=headers, files=form_data)
def generate_ai_image(prompt):
    headers = {
        "Authorization": f"Bearer {STABILITY_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"  # Add this
    }
    
    # Correct payload structure for SDXL 1.0
    payload = {
        "text_prompts": [
            {
                "text": f"{prompt}, {GENRE}, 4k, trending on ArtStation",
                "weight": 0.5
            }
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "steps": 30,
        "samples": 1,
        "style_preset": "digital-art"  # Add style preset
    }

    response = requests.post(STABILITY_API, headers=headers, json=payload) 
    if response.status_code == 200:
        json_data = response.json()
        if "artifacts" in json_data:
            # Stability AI returns base64-encoded image
            image_data = json_data["artifacts"][0]["base64"]
            return save_image(image_data)
    print(f"Generation failed: {response.text}")
    return None

def save_image(base64_str, filename="temp_post.jpg"):
    """Decodes base64 image and saves it locally."""
    image_bytes = base64.b64decode(base64_str)
    with open(filename, "wb") as f:
        f.write(image_bytes)
    return filename


    
def post_to_instagram(image_path,caption):
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
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error: {e} ye hai erroror")
        time.sleep(2 * 60 * 60)  # Wait 2 hours before posting again
