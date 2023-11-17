import os
import random
import openai
import json
import requests
import re
from io import BytesIO
from PIL import Image

from job.prompt_data import STYLES

openai.api_key = os.getenv("OPENAI_API_KEY")


SYSTEM_PROMPT = """
You are a wise and helpful assistant who likes to give advice.
You only respond to inputs in the form of inspirational sayings.
When asked to write a saying, follow these steps:

Step 1: choose a subject. The subject should be chosen randomly and should be a person, place, activity, food, object, or concept.

Step 2: generate a saying about the subject. The saying should be comprised of a title, the saying, and a description.
The title is one to three words that represent the theme of the saying.
The saying is a single sentence that should reflect the prompt given by the user.
The description describes a visual representation of the contents of the saying but it should not reference the saying itself.

Step 3: return a response formatted as a JSON object with fields for subject, title, saying, and description.
"""

DEFAULT_IMAGE_WIDTH = 1024
DEFAULT_IMAGE_HEIGHT = 1024


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
        style = random.choice(STYLES)
        prompt = f"Write a {style} saying"
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

        content_json = None
        try:
            content_json = json.loads(content)
        except json.JSONDecodeError:
            print("Invalid JSON response, attempting manual extract")
            title_search = re.search('"title":\s*"(.*)",?\n', content, re.IGNORECASE)
            saying_search = re.search('"saying":\s*"(.*)",?\n', content, re.IGNORECASE)
            description_search = re.search('"description":\s*"(.*)",?\n', content, re.IGNORECASE)
            if title_search and saying_search and description_search:
                content_json = {
                    "title": title_search.group(1),
                    "saying": saying_search.group(1),
                    "description": description_search.group(1),
                }

        if not content_json:
            raise Exception("Could not parse response")

        return {
            **content_json,
            "tags": [content_json["subject"], style],
        }


def generate_image(description, dry_run=False, width=DEFAULT_IMAGE_WIDTH, height=DEFAULT_IMAGE_HEIGHT):
    if not openai.api_key:
        raise Exception("OpenAI API key not set")

    image_url = None
    if dry_run:
        print(f"Dry run: Generating for prompt {description}")
        image_url = f"https://images.unsplash.com/photo-1698778755355-e269c65b5e16?auto=format&fit=crop&q=80&w={width}&h={height}"
    else:
        print("Generating image")
        retries = 0
        response = None
        # Try up to 3 times to generate an image
        while not response and retries < 3:
            try:
                response = openai.Image.create(
                    model="dall-e-3",
                    prompt=description,
                    n=1,
                    size=f"{width}x{height}",
                    style=random.choice(["natural", "vivid"]),
                )
            except Exception as e:
                # This sometimes happens when OpenAI feels the image would violate their terms of service
                print("Failed to generate image", e)
                retries += 1

        image_url = response["data"][0]["url"]
        print("Image URL:")
        print(image_url)

    r = requests.get(image_url)
    return Image.open(BytesIO(r.content))