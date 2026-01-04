from config import config
import random
import os


import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask
# import PIL.ImageOps

# alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'

openai_model = "gpt-3.5-turbo"

# def random_choice():
#     return ''.join(random.choices(alphabet, k=8))
#
# def generate_codes(quantity=10):
#     for i in range(quantity):
#         qr = qrcode.QRCode(
#             version=1,
#             box_size=50,
#         )
#         shortcode = random_choice()
#         qr.add_data("https://youtu.be/dQw4w9WgXcQ?t=40")
#
#         img = qr.make_image(
#             # box_size=40,
#             image_factory=StyledPilImage,
#             module_drawer=RoundedModuleDrawer(),
#             eye_drawer=RoundedModuleDrawer(),
#             color_mask=SolidFillColorMask(back_color=(255, 255, 255, 0), front_color=(84, 84, 84, 255)),
#         )
#
#         # img = PIL.ImageOps.invert(img)
#         img.save("./scratchdir/{}.png".format(shortcode))


def generate_code(filename, url, color_tuple):

    qr = qrcode.QRCode(
        version=1,
        box_size=50,
    )

    qr.add_data(url)

    img = qr.make_image(
        # box_size=40,
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        eye_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=(255, 255, 255, 0), front_color=color_tuple),
    )

    # img = PIL.ImageOps.invert(img)
    img.save("./scratchdir/{}.png".format(filename))


def generate_dumbquote():

    authors = [
        "Buddha's second husband",
        "Buddha's third husband",
        "Buddha's fifth husband",
        "Buddha's drug dealer",
        "Jesus, probably",
        "The third wife of Jesus",
        "Nobody really knows",
        "Some human, maybe. AI took over...",
        "A Rabbi, I think",
        "The REAL Dalai Lama",
        "The Dalai Lama's stunt double",
        "Gandhi's secret twin",
        "Gandhi's astrology coach",
        "Plato’s funky cousin",
        "Probably Einstein's barber",
        "The Pope's dope niece",
        "The Pope's distant cousin twice removed",
        "A random catholic monk",
        "Aristotle's long-lost roommate",
        "Zeus' yoga instructor",
        "Newton's apple dealer",
        "Newton's gravity consultant",
        "Mozart’s backup singer",
        "Mozart’s ghostwriter",
    ]

    author = random.choice(authors)

    messages = [
        {"role": "system", "content": "You are a person with witty and sarcastic humor"},
        {"role": "user", "content":
            """Generate a stupid life tip.
            Return only whatever advice you generate and don't include em dashes.
            Place it between quotation marks."""}
    ]

    completion = config.clients.openai.chat.completions.create(
        model=openai_model,
        messages=messages
    )

    quote = completion.choices[0].message.content

    return quote, author

def generate_icebreaker():
    messages = [
        {"role": "system", "content": "You are a genuinely curious person who is good at listening to people"},
        {"role": "user", "content":
            """Generate an open-ended question to be used as an icebreaker. \
            The person who is asked the question should be likely to respond with a personal story. \
            Return only whatever question you generate and don't include em dashes. \
            Place it between quotation marks."""}
    ]

    completion = config.clients.openai.chat.completions.create(
        model=openai_model,
        messages=messages
    )

    icebreaker = completion.choices[0].message.content

    return icebreaker

def list_image_files(directory):
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_files.append(os.path.join("./", directory, filename))
    return image_files

def random_images(images_dir = 'examples', quantity = 1, ):
    set = list_image_files('static/images/' + images_dir)
    random_set = random.sample(set, quantity)
    random.shuffle(random_set)
    return random_set

# print(random_images('examples', quantity=2))

if __name__ == '__main__':
    generate_code('code','https://calendly.com/rileysbudd/30min',(255,209,89,255))