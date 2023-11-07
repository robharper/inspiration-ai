import os
import random
import openai
import json
import requests
from io import BytesIO
from PIL import Image

from job.prompt_data import SUBJECTS, STYLES

openai.api_key = os.getenv("OPENAI_API_KEY")


SYSTEM_PROMPT = """You are a wise and helpful assistant who likes to give advice.
You only respond to inputs in the form of inspirational sayings.
All responses are comprised of three parts: a title, a saying, and a description.
The title is one to three words that represent the theme of the saying.
The saying is a single sentence that should reflect the prompt given by the user.
The description describes how the saying would look if it were an image.
Responses should be formatted as a JSON object with fields for title, saying, and description."""

DEFAULT_IMAGE_WIDTH = 512
DEFAULT_IMAGE_HEIGHT = 512


def generate_quote(dry_run=False):
    if not openai.api_key:
        raise Exception("OpenAI API key not set")

    if dry_run:
        print(f"Dry run: Returning fake AI response")
        return {
            "title": "Inspiration",
            "saying": "This is a dry run. It should be very inspiring.",
            "description": "A dry desert with no water in sight",
            "tags": ["dry", "desert", "inspiration"],
        }
    else:
        subject = random.choice(SUBJECTS)
        style = random.choice(STYLES)
        prompt = f"Write a {style} saying about {subject}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # Higher temperature to get less predicatable results
            temperature=1.5,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]
        )
        content = response["choices"][0]["message"]["content"]
        print("GPT-3 Response:")
        print(content)
        try:
            return {
                **json.loads(content),
                "tags": [subject, style],
            }
        except json.JSONDecodeError:
            print("Invalid JSON response")
            print(content)
            return {
                "title": "AI Fails You",
                "saying": "Ask for JSON, get garbage.",
                "description": "A sad robot with his head hanging down trying to read code.",
                "tags": [subject, style],
            }


def generate_image(description, dry_run=False, width=DEFAULT_IMAGE_WIDTH, height=DEFAULT_IMAGE_HEIGHT):
    if not openai.api_key:
        raise Exception("OpenAI API key not set")

    image_url = None
    if dry_run:
        print(f"Dry run: Returning static image")
        image_url = f"https://images.unsplash.com/photo-1698778755355-e269c65b5e16?auto=format&fit=crop&q=80&w={width}&h={height}"
    else:
        print("Generating image")
        response = openai.Image.create(
            prompt=description,
            n=1,
            size=f"{width}x{height}"
        )
        image_url = response["data"][0]["url"]
        print("Image URL:")
        print(image_url)

    r = requests.get(image_url)
    return Image.open(BytesIO(r.content))