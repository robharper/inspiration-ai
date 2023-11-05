from PIL import Image, ImageFont, ImageDraw

FONT_SIZE = 60
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
IMAGE_OUT_WIDTH = 1024
IMAGE_OUT_HEIGHT = 512
TEXT_MARGIN = 20


def build_image(quote_data, background):
    """
    Embed the quote text onto the background image
    """
    title, quote = quote_data["title"], quote_data["quote"]

    # Extend the background image to create a text area on the right
    image = Image.new("RGB", (IMAGE_OUT_WIDTH, IMAGE_OUT_HEIGHT))
    image.paste(background, (0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))

    font = ImageFont.load_default(FONT_SIZE)
    draw = ImageDraw.Draw(image)

    title_size = draw.multiline_textbbox((0,0), title, font=font)
    quote_size = draw.multiline_textbbox((0,0), quote, font=font, align="center")

    draw.text((IMAGE_WIDTH + TEXT_MARGIN + title_size[0]/2, TEXT_MARGIN), quote_data["title"], (255, 255, 255), font=font)
    draw.text((IMAGE_WIDTH + TEXT_MARGIN, IMAGE_HEIGHT/2), quote_data["quote"], (255, 255, 255), font=font)
    return image
