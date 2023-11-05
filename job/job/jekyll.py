from yaml import dump


def build_page(date, quote, image_url):
    front_matter = {
        "layout": "post",
        "quote_title": quote["title"],
        "quote_image_url": image_url,
        "tags": quote["tags"],
    }

    return dump(front_matter) + "\n---\n\n" + quote["saying"]