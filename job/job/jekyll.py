from yaml import dump


def build_page(date, quote, image_url):
    # TODO build title with date

    front_matter = {
        "layout": "post",
        "quote_title": quote["title"],
        "quote_image_url": image_url,
    }

    return dump(front_matter) + "\n---\n\n" + quote["quote"]