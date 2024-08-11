from config import config
import random

openai_model = "gpt-3.5-turbo"

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

