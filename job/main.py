import os
import openai
import functions_framework
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")
DRY_RUN = os.getenv("DRY_RUN", False)

SYSTEM_PROMPT = '''You are a wise and helpful assistant.
You only respond to inputs in the form of inspirational quotes.
All responses are comprised of three parts: a title, a quote, and a description.
The title is one or two words that represent the theme of the quote.
The quote is a single sentence that is the inspirational quote itself.
The description describes how the quote would look if it were an image.
Responses should be formatted as a JSON object with fields for title, quote, and description.'''

PROMPT = 'Write an inspirational quote about cats'

FONT_SIZE = 60
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
IMAGE_OUT_WIDTH = 1024
IMAGE_OUT_HEIGHT = 512
TEXT_MARGIN = 20

def generate_quote():
    if DRY_RUN:
        return {
            "title": "Inspiration",
            "quote": "This is a dry run. It should be very inspiring.",
            "description": "A dry desert with no water in sight",
        }
    else:
        # TODO
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": PROMPT},
            ]
        )
        content = response['choices'][0]['message']['content']


def generate_image_background(description):
    image_url = None
    if DRY_RUN:
        image_url = f'https://images.unsplash.com/photo-1698778755355-e269c65b5e16?auto=format&fit=crop&q=80&w={IMAGE_WIDTH}&h={IMAGE_HEIGHT}'
    else:
        # TODO
        response = openai.Image.create(
            prompt=description,
            n=1,
            size=f'{IMAGE_WIDTH}x{IMAGE_HEIGHT}'
        )
        image_url = response['data'][0]['url']

    r = requests.get(image_url)
    return Image.open(BytesIO(r.content))


def build_image(quote_data, background):
    """
    Embed the quote text onto the background image
    """
    title, quote = quote_data['title'], quote_data['quote']

    # Extend the background image to create a text area on the right
    image = Image.new('RGB', (IMAGE_OUT_WIDTH, IMAGE_OUT_HEIGHT))
    image.paste(background, (0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))

    font = ImageFont.load_default(FONT_SIZE)
    draw = ImageDraw.Draw(image)

    title_size = draw.multiline_textbbox((0,0), title, font=font)
    quote_size = draw.multiline_textbbox((0,0), quote, font=font, align='center')

    draw.text((IMAGE_WIDTH + TEXT_MARGIN + title_size[0]/2, TEXT_MARGIN), quote_data['title'], (255, 255, 255), font=font)
    draw.text((IMAGE_WIDTH + TEXT_MARGIN, IMAGE_HEIGHT/2), quote_data['quote'], (255, 255, 255), font=font)
    return image

def upload_image(image):
    if DRY_RUN:
        filename = "result.jpg"
        image.save(filename)
        return filename
    else:
        pass

# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def generate_inspiration(cloud_event):
    if not openai.api_key:
        raise Exception("OpenAI API key not set")

    # Generate the inspirational quote
    quote_data = generate_quote()

    # Create the inspirational image
    background = generate_image_background(quote_data["description"])
    image = build_image(quote_data, background)

    # Upload the image
    image_url = upload_image(image)

    # Generate the markdown

    # Upload the markdown