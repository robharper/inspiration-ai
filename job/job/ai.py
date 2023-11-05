import os
import openai
import json
import requests
from io import BytesIO
from PIL import Image

openai.api_key = os.getenv("OPENAI_API_KEY")


SYSTEM_PROMPT = """You are a wise and helpful assistant.
You only respond to inputs in the form of inspirational quotes.
All responses are comprised of three parts: a title, a quote, and a description.
The title is one or two words that represent the theme of the quote.
The quote is a single sentence that is the inspirational quote itself.
The description describes how the quote would look if it were an image.
Responses should be formatted as a JSON object with fields for title, quote, and description."""

# TODO
PROMPT = "Write an inspirational quote about cats"

DEFAULT_IMAGE_WIDTH = 512
DEFAULT_IMAGE_HEIGHT = 512


def generate_quote(dry_run=False):
    if not openai.api_key:
        raise Exception("OpenAI API key not set")

    if dry_run:
        return {
            "title": "Inspiration",
            "quote": "This is a dry run. It should be very inspiring.",
            "description": "A dry desert with no water in sight",
        }
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": PROMPT},
            ]
        )
        content = response["choices"][0]["message"]["content"]
        print("GPT-3 Response:")
        print(content)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Invalid JSON response")
            print(content)
            return {
                "title": "AI Fails You",
                "quote": "Ask for JSON, get garbage.",
                "description": "A sad robot with his head hanging down trying to read code.",
            }


def generate_image(description, dry_run=False, width=DEFAULT_IMAGE_WIDTH, height=DEFAULT_IMAGE_HEIGHT):
    if not openai.api_key:
        raise Exception("OpenAI API key not set")

    image_url = None
    if dry_run:
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