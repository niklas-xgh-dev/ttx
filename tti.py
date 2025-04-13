from pathlib import Path
import os
import base64
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client - it will automatically use the OPENAI_API_KEY environment variable
client = OpenAI()

# Set output path
output_dir = Path(__file__).parent
output_file = output_dir / "generated_image.png"

# Create the image
response = client.images.generate(
    model=os.getenv("IMAGE_MODEL"),
    prompt="Create me a broke software dev in a california cafe. funny, edgy humor and trist",
    n=1,
    size=os.getenv("IMAGE_SIZE"),
    quality=os.getenv("IMAGE_QUALITY"),
    response_format=os.getenv("IMAGE_FORMAT"),  # "url" or "b64_json"
    style=os.getenv("IMAGE_STYLE"),  # "vivid" or "natural"
)

# Get the generated image data
image_data = response.data[0]

# Save the image based on response format
if hasattr(image_data, 'url') and image_data.url:
    # If response format is URL, download the image
    image_url = image_data.url
    print(f"Image URL: {image_url}")
    
    # Download the image
    img_response = requests.get(image_url)
    if img_response.status_code == 200:
        with open(output_file, "wb") as img_file:
            img_file.write(img_response.content)
        print(f"Image saved to {output_file}")
    else:
        print(f"Failed to download image: {img_response.status_code}")
        
elif hasattr(image_data, 'b64_json') and image_data.b64_json:
    # If response format is b64_json, decode and save
    img_data = base64.b64decode(image_data.b64_json)
    with open(output_file, "wb") as img_file:
        img_file.write(img_data)
    print(f"Image saved to {output_file}")
else:
    print("No image data found in the response")